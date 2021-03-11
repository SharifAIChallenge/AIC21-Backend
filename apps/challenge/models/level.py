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

    @staticmethod
    def create_levels_for_level_based_tournament(level_based_tournament, count):
        levels = []
        for i in range(count):
            lvl = Level(number=i+1, level_based_tournament=level_based_tournament)
            levels.append(lvl)

        return levels
