from django.db import models
from model_utils.models import TimeStampedModel


class LobbyTypes:
    FRIENDLY_MATCH = 'friendly_match'
    LEVEL_BASED_TOURNAMENT = 'level_based_tournament'
    TYPES = (
        (FRIENDLY_MATCH, 'Friendly match'),
        (LEVEL_BASED_TOURNAMENT, 'Level based tournament'),
    )


class LobbyQueue(TimeStampedModel):
    team = models.OneToOneField(to='team.Team', on_delete=models.CASCADE,
                                related_name='lobby_queue')
    game_type = models.CharField(
        max_length=50,
        choices=LobbyTypes.TYPES,
        default=LobbyTypes.FRIENDLY_MATCH
    )

    @staticmethod
    def get_lobby_population(game_type):
        return LobbyQueue.objects.filter(
            game_type=game_type
        ).count()
