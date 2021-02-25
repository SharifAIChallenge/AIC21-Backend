from django.db import models
from model_utils.models import TimeStampedModel


class TournamentTypes:
    NORMAL = 'successful'
    FRIENDLY = 'friendly'
    CLANWAR = 'clanwar'
    TYPES = (
        (NORMAL, 'Normal'),
        (FRIENDLY, 'Friendly'),
        (CLANWAR, 'Clanwar')
    )


class Tournament(TimeStampedModel):
    name = models.CharField(max_length=512)
    types = models.CharField(
        max_length=50,
        choices=TournamentTypes.TYPES,
        default=TournamentTypes.NORMAL
    )
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    is_hidden = models.BooleanField(default=False)

    def init_tournament(self, team_list):
        pass
