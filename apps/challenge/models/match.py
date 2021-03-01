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
    team1 = models.ForeignKey(to='team.Team', on_delete=models.CASCADE, related_name='matches_first')
    team2 = models.ForeignKey(to='team.Team', on_delete=models.CASCADE, related_name='matches_second')
    status = models.CharField(
        max_length=50,
        choices=MatchStatusTypes.TYPES,
        default=MatchStatusTypes.RUNNING
    )
    winner = models.ForeignKey(to='team.Team', on_delete=models.CASCADE, related_name='won_matches', null=True, blank=True)
    log = models.FileField(upload_to=settings.UPLOAD_PATHS['MATCH_LOGS'], null=True, blank=True)
    tournament = models.ForeignKey(to='challenge.Tournament', on_delete=models.CASCADE, related_name='matches')

    @property
    def is_freeze(self):
        return self.status == MatchStatusTypes.FREEZE

    def run_match(self):
        pass

    @staticmethod
    def run_matches(matches):
        pass

    @staticmethod
    def create_match(team1, team2, tournament, match_map):
        pass

