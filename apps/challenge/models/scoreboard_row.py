from django.db import models
from model_utils.models import TimeStampedModel


class ScoreboardRow(TimeStampedModel):
    scoreboard = models.ForeignKey(to='challenge.Scoreboard', on_delete=models.CASCADE, related_name='rows')
    team = models.ForeignKey(to='team.Team', on_delete=models.RESTRICT, related_name='scoreboard_rows')
    score = models.PositiveIntegerField(default=0)
    wins = models.PositiveIntegerField(default=0)
    losses = models.PositiveIntegerField(default=0)
    draws = models.PositiveIntegerField(default=0)
