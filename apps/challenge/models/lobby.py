from django.db import models
from model_utils.models import TimeStampedModel


class LobbyTypes:
    FRIENDLY_MATCH = 'friendly_match'
    LEVEL_BASED_TOURNAMENT = 'level_based_tournament'
    TYPES = (
        (FRIENDLY_MATCH, 'Friendly match'),
        (LEVEL_BASED_TOURNAMENT, 'Level based tournament'),
    )
    TYPES_ARR = list(dict(TYPES).keys())


class LobbyQueue(TimeStampedModel):
    team = models.ForeignKey(to='team.Team', on_delete=models.CASCADE,
                                related_name='lobby_queues')
    game_type = models.CharField(
        max_length=50,
        choices=LobbyTypes.TYPES,
    )

    def get_lobby_population(self):
        return LobbyQueue.objects.filter(
            game_type=self.game_type
        ).count()

    def get_lobby_size(self):  # TODO : Read from config
        if self.game_type == LobbyTypes.FRIENDLY_MATCH:
            return 2

        return 8
