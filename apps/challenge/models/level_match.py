from django.db import models
from model_utils.models import TimeStampedModel


class LevelMatch(TimeStampedModel):
    match = models.OneToOneField(
        to='challenge.Match',
        on_delete=models.RESTRICT,
        related_name='level_match'
    )
    level = models.ForeignKey(
        to='challenge.Level',
        on_delete=models.CASCADE,
        related_name='level_matches'
    )

    @staticmethod
    def create_level_matches(match_list, level):
        level_matches = []

        for match in match_list:
            level_match = LevelMatch.objects.create(
                match=match,
                level=level
            )
            level_matches.append(level_match)

        return level_matches

