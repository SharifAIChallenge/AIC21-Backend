from django.db import models
from model_utils.models import TimeStampedModel

from apps.challenge.models import Tournament, Level
import math


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

    def check_level(self):
        pass

    @staticmethod
    def create_level_based_tournament(name, start_time, end_time, is_hidden,
                                      is_friendly=False, team_list=None,
                                      is_scoreboard_freeze=False, size=8):

        def is_power_of_two(n):
            return (n & (n-1) == 0) and n != 0

        if not is_power_of_two(size):
            raise Exception("Size should be power of two")

        tournament = Tournament.create_tournament(name, start_time, end_time, is_hidden,
                                                  is_friendly, team_list,
                                                  is_scoreboard_freeze)

        level_based_tournament = LevelBasedTournament(tournament=tournament, size=size)

        levels = Level.create_levels_for_level_based_tournament(level_based_tournament, math.log(size))

        # TODO : Do other needed stuff ...
