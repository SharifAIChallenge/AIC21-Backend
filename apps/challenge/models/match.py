from django.db import models
from model_utils.models import TimeStampedModel
from django.conf import settings
from rest_framework.generics import get_object_or_404

from apps.challenge.models.tournament import TournamentTypes


class MatchStatusTypes:
    FREEZE = 'freeze'
    PENDING = 'pending'
    FAILED = 'failed'
    SUCCESSFUL = 'successful'
    RUNNING = 'running'
    TYPES = (
        (FAILED, 'Failed'),
        (SUCCESSFUL, 'Successful'),
        (RUNNING, 'Running'),
        (FREEZE, 'Freeze'),
        (PENDING, 'pending')
    )


class Match(TimeStampedModel):
    team1 = models.ForeignKey(to='team.Team', on_delete=models.CASCADE,
                              related_name='matches_first')
    team2 = models.ForeignKey(to='team.Team', on_delete=models.CASCADE,
                              related_name='matches_second')
    status = models.CharField(
        max_length=50,
        choices=MatchStatusTypes.TYPES,
        default=MatchStatusTypes.FREEZE
    )
    winner = models.ForeignKey(to='team.Team', on_delete=models.CASCADE,
                               related_name='won_matches', null=True,
                               blank=True)
    log = models.FileField(upload_to=settings.UPLOAD_PATHS['MATCH_LOGS'],
                           null=True, blank=True)
    log_file_token = models.CharField(max_length=256, null=True, blank=True)
    tournament = models.ForeignKey(
        to='challenge.Tournament',
        on_delete=models.CASCADE,
        related_name='matches'
    )

    infra_token = models.CharField(
        max_length=256,
        blank=True,
        null=True
    )

    @property
    def is_freeze(self):
        return self.status == MatchStatusTypes.FREEZE

    @property
    def is_successful(self):
        return self.status == MatchStatusTypes.SUCCESSFUL

    @classmethod
    def update_match(cls, infra_token, status):
        match = get_object_or_404(
            cls, infra_token=infra_token
        )
        match.status = status
        match.save()

        return match

    def run_match(self):
        from apps.infra_gateway.functions import run_match
        self.infra_token = run_match(
            match=self
        )
        self.save()

    @staticmethod
    def run_matches(matches):
        for match in matches:
            match.run_match()

    @staticmethod
    def create_match(team1, team2, tournament, match_map, is_freeze=False):
        from apps.challenge.models import MatchInfo

        team1_final_submission = team1.final_submission()
        team2_final_submission = team2.final_submission()

        if team1_final_submission and team2_final_submission:
            match = Match.objects.create(
                team1=team1,
                team2=team2,
                status=MatchStatusTypes.PENDING
                if not is_freeze else MatchStatusTypes.FREEZE,
                tournament=tournament
            )
            match_info = MatchInfo.objects.create(
                team1_code=team1_final_submission,
                team2_code=team2_final_submission,
                match=match,
                map=match_map
            )

            if not is_freeze:
                match.run_match()

            return match
        return None

    @staticmethod
    def create_match_from_list(teams, tournament, match_map):
        if len(teams) % 2 == 1:
            raise Exception('teams list size must be even not odd!')

        i = 0
        matches = []
        while i < len(teams):
            team1 = teams[i]
            team2 = teams[i + 1]
            match = Match.create_match(
                team1=team1,
                team2=team2,
                tournament=tournament,
                match_map=match_map
            )
            matches.append(match)

        return matches

    @staticmethod
    def create_friendly_match(team1, team2, game_map=None):
        from apps.challenge.models import Map, Tournament

        if game_map is None:
            game_map = Map.get_random_map()
        friendly_tournament = Tournament.get_friendly_tournament()

        if friendly_tournament is None:
            raise Exception(
                "Admin should initialize a friendly tournament first ...")

        Match.create_match(team1, team2, friendly_tournament, game_map)

    @property
    def game_log(self):
        from apps.infra_gateway.functions import download_log
        return 'https://google.com'
        # return download_log(
        #     match_infra_token=self.infra_token
        # )

    @property
    def team1_log(self):
        from apps.infra_gateway.functions import download_log

        return download_log(
            match_infra_token=self.infra_token,
            file_infra_token=self.match_info.team1_code
        )

    @property
    def team2_log(self):
        from apps.infra_gateway.functions import download_log

        return download_log(
            match_infra_token=self.infra_token,
            file_infra_token=self.match_info.team2_code
        )
