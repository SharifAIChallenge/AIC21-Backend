from django.db import models
from model_utils.models import TimeStampedModel


class LevelBasedTournament(TimeStampedModel):
    tournament = models.OneToOneField(
        to='challenge.Tournament',
        on_delete=models.RESTRICT,
        related_name='level_based_tournament'
    )
    size = models.PositiveSmallIntegerField(default=8)

    @property
    def get_last_level(self):
        return 0  # TODO
