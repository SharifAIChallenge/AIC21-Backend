from django.db import models
from model_utils.models import TimeStampedModel
from django.conf import settings


class Clan(TimeStampedModel):
    IMAGE_MAX_SIZE = 1024 * 1024

    name = models.CharField(max_length=256, unique=True)
    leader = models.OneToOneField(to='team.Team', on_delete=models.RESTRICT, related_name='owned_clan')
    image = models.ImageField(upload_to=settings.UPLOAD_PATHS['CLAN_IMAGE'], null=True, blank=True)
    score = models.PositiveIntegerField(default=0)
    wins = models.PositiveIntegerField(default=0)
    losses = models.PositiveIntegerField(default=0)
    draws = models.PositiveIntegerField(default=0)
