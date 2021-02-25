from django.db import models
from model_utils.models import TimeStampedModel


class MatchInfo(TimeStampedModel):
    team1_score = models.PositiveIntegerField()
    team2_score = models.PositiveIntegerField()
    # TODO : Team1 Code
    # TODO : Team2 Code
    match_duration = models.DurationField()
    match = models.OneToOneField(to='challenge.Match', on_delete=models.CASCADE, related_name='match_info')
    map = models.ForeignKey(to='challenge.Map', on_delete=models.CASCADE, related_name='match_info')
