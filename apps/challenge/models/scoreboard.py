from django.db import models
from model_utils.models import TimeStampedModel


class Scoreboard(TimeStampedModel):
    tournament = models.OneToOneField(to='challenge.Tournament',
                                      on_delete=models.CASCADE,
                                      related_name='scoreboard')
    freeze = models.BooleanField(default=False)
