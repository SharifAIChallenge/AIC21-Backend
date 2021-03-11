from django.db import models
from model_utils.models import TimeStampedModel


class MatchInfo(TimeStampedModel):
    team1_score = models.PositiveIntegerField(
        blank=True,
        null=True
    )
    team2_score = models.PositiveIntegerField(
        blank=True,
        null=True
    )
    team1_code = models.ForeignKey(
        to='team.Submission',
        related_name='matches_first',
        on_delete=models.SET_NULL,
        null=True
    )
    team2_code = models.ForeignKey(
        to='team.Submission',
        related_name='matches_second',
        on_delete=models.SET_NULL,
        null=True
    )
    match_duration = models.PositiveSmallIntegerField(
        blank=True,
        null=True
    )
    match = models.OneToOneField(
        to='challenge.Match',
        on_delete=models.CASCADE,
        related_name='match_info'
    )
    map = models.ForeignKey(
        to='challenge.Map',
        on_delete=models.CASCADE,
        related_name='match_info'
    )
