from django.db import models
from model_utils.models import TimeStampedModel
from django.conf import settings


class MatchStatusTypes:
    FREEZE = 'freeze'
    FAILED = 'failed'
    SUCCESSFUL = 'successful'
    RUNNING = 'running'
    TYPES = (
        (FAILED, 'Failed'),
        (SUCCESSFUL, 'Successful'),
        (RUNNING, 'Running'),
        (FREEZE, 'Freeze')
    )


class Match(TimeStampedModel):
    team1 = models.ForeignKey(to='team.Team', on_delete=models.CASCADE,
                              related_name='matches_first')
    team2 = models.ForeignKey(to='team.Team', on_delete=models.CASCADE,
                              related_name='matches_second')
    status = models.CharField(
        max_length=50,
        choices=MatchStatusTypes.TYPES,
        default=MatchStatusTypes.RUNNING
    )
    winner = models.ForeignKey(to='team.Team', on_delete=models.CASCADE,
                               related_name='won_matches', null=True,
                               blank=True)
    log = models.FileField(upload_to=settings.UPLOAD_PATHS['MATCH_LOGS'],
                           null=True, blank=True)
    tournament = models.ForeignKey(to='challenge.Tournament',
                                   on_delete=models.CASCADE,
                                   related_name='matches')

    @property
    def is_freeze(self):
        return self.status == MatchStatusTypes.FREEZE

    @property
    def is_finished(self):
        return self.status == MatchStatusTypes.SUCCESSFUL

    def run_match(self):
        pass

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
                status=MatchStatusTypes.RUNNING
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
