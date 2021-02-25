from django.db import models


class Level(models.Model):
    number = models.PositiveSmallIntegerField()
    level_based_tournament = models.ForeignKey(
        to='challenge.LevelBasedTournament',
        on_delete=models.CASCADE,
        related_name='level'
    )

    @property
    def is_finished(self):
        return False  # TODO
