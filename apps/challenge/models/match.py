import math

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
    def update_match(cls, infra_token, status, message=None, stats=None):
        match: 'Match' = get_object_or_404(
            cls, infra_token=infra_token
        )

        if message:
            match.message = message

        if stats and not match.winner:
            winner = stats.get('winner', 0)
            if winner == 0:
                match.winner = match.team1
            elif winner == 1:
                match.winner = match.team2

            match.update_score()

        match.status = status
        match.save()

        return match

    def run_match(self, priority=0):
        from apps.infra_gateway.functions import run_match
        self.infra_token = run_match(
            match=self,
            priority=priority
        )
        self.save()

    @staticmethod
    def run_matches(matches, priority=0):
        for match in matches:
            match.run_match(priority=priority)

    @staticmethod
    def create_match(team1, team2, tournament, match_map, is_freeze=False,
                     priority=0):
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
                match.run_match(priority=priority)

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

        return Match.create_match(team1, team2, friendly_tournament, game_map,
                                  priority=1)

    @staticmethod
    def create_bot_match(bot, team, game_map=None):
        from apps.challenge.models import Map, Tournament

        if game_map is None:
            game_map = Map.get_random_map()
        bot_tournament = Tournament.get_bot_tournament()

        if bot_tournament is None:
            raise Exception(
                "Admin should initialize a bot tournament first ..."
            )

        return Match.create_match(bot, team, bot_tournament, game_map,
                                  priority=1)

    @property
    def game_log(self):
        from apps.infra_gateway.functions import download_log

        if self.status == MatchStatusTypes.SUCCESSFUL:
            return download_log(
                match_infra_token=self.infra_token
            )

        return ''

    @property
    def server_log(self):
        from apps.infra_gateway.functions import download_log

        if self.status not in [MatchStatusTypes.FREEZE,
                               MatchStatusTypes.PENDING,
                               MatchStatusTypes.RUNNING]:
            return download_log(
                match_infra_token=self.infra_token,
                file_infra_token=f'{self.infra_token}.out'
            )
        return ''

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

    @property
    def winner_number(self):
        if self.winner == self.team1:
            return 1
        if self.winner == self.team2:
            return 2

    def update_score(self, k=30):
        if self.tournament.scoreboard.freeze:
            return
        winner_number = self.winner_number

        team1_row = self.tournament.scoreboard.get_team_row(team=self.team1)
        team2_row = self.tournament.scoreboard.get_team_row(team=self.team2)

        p1 = (1.0 / (1.0 + math.pow(
            10,
            (team2_row.score - team1_row.score) / 400
        )))
        p2 = (1.0 / (1.0 + math.pow(
            10,
            (team1_row.score - team2_row.score) / 400
        )))

        if self.tournament.type not in [TournamentTypes.NORMAL,
                                        TournamentTypes.FINAL]:
            team1_row.score = team1_row.score + k * (2 - winner_number - p1)
            team2_row.score = team2_row.score + k * (winner_number - 1 - p2)
        else:
            if winner_number == 1:
                team1_row.score += 15
            elif winner_number == 2:
                team2_row.score += 15

        if winner_number == 1:
            team1_row.wins += 1
            team2_row.losses += 1
        elif winner_number == 2:
            team2_row.wins += 1
            team1_row.losses += 1

        team1_row.save()
        team2_row.save()
