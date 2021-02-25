from django.db import models
from model_utils.models import TimeStampedModel
from django.conf import settings


class MatchStatusTypes:
    FAILED = 'failed'
    SUCCESSFUL = 'successful'
    RUNNING = 'running'
    TYPES = (
        (FAILED, 'Failed'),
        (SUCCESSFUL, 'Successful'),
        (RUNNING, 'Running')
    )


class Match(TimeStampedModel):
    team1 = models.ForeignKey(to='team.Team', on_delete=models.CASCADE, related_name='matches_first')
    team2 = models.ForeignKey(to='team.Team', on_delete=models.CASCADE, related_name='matches_second')
    status = models.CharField(
        max_length=50,
        choices=MatchStatusTypes.TYPES,
        default=MatchStatusTypes.RUNNING
    )
    winner = models.ForeignKey(to='team.Team', on_delete=models.CASCADE, related_name='won_matches')
    log = models.FileField(upload_to=settings.UPLOAD_PATHS['MATCH_LOGS'], null=True, blank=True)
    tournament = models.ForeignKey(to='challenge.Tournament', on_delete=models.CASCADE, related_name='matches')
    is_freeze = models.BooleanField(default=True)


