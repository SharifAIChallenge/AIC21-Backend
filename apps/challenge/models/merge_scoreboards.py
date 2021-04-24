from django.db import models


class MergeScoreboards(models.Model):
    src = models.ForeignKey(
        'challenge.Tournament',
        related_name='src_merges',
        on_delete=models.CASCADE
    )
    dest = models.ForeignKey(
        'challenge.Tournament',
        related_name='dest_merges',
        on_delete=models.CASCADE
    )

    coef = models.FloatField(
        default=1.0
    )

    cost = models.IntegerField(
        default=1000
    )

    def pre_save(self):
        from apps.challenge.models import Scoreboard
        Scoreboard.merge_scoreboards(
            self.src.scoreboard,
            self.dest.scoreboard
        )

    def save(self, *args, **kwargs):
        self.pre_save()
        super(MergeScoreboards, self).save(*args, **kwargs)
