from django.db import models
from model_utils.models import TimeStampedModel, UUIDModel
from django.conf import settings


class Map(TimeStampedModel, UUIDModel):
    name = models.CharField(
        max_length=256,
        unique=True
    )
    file = models.FileField(
        upload_to=settings.UPLOAD_PATHS["MAP"]
    )
    active = models.BooleanField(default=True)

    @staticmethod
    def get_random_map():
        game_map = Map.objects.filter(active=True).order_by('?').first()
        if game_map is None:
            raise Exception("There is no map available in the database")

        return game_map
