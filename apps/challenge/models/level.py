from django.db import models


class Level(models.Model):
    number = models.PositiveSmallIntegerField(default=1)
    level_based_tournament = models.ForeignKey(
        to='challenge.LevelBasedTournament',
        on_delete=models.CASCADE,
        related_name='levels'
    )

    @property
    def is_finished(self):
        from apps.challenge.models import MatchStatusTypes

        return self.level_matches.count() == self.level_matches.filter(
            match__status=MatchStatusTypes.SUCCESSFUL
        ).count()

    @staticmethod
    def create_level(matches, tournament, last_level: 'Level' = None):
        from apps.challenge.models import LevelMatch

        level = Level.objects.create(
            number=1 if not last_level else last_level.number + 1,
            level_based_tournament=tournament
        )
        LevelMatch.create_level_matches(
            match_list=matches,
            level=level
        )
        return level

    @staticmethod
    def create_levels_for_level_based_tournament(level_based_tournament,
                                                 count):
        levels = []
        for i in range(count):
            lvl = Level.objects.create(
                number=i + 1,
                level_based_tournament=level_based_tournament
            )
            levels.append(lvl)

        return levels
