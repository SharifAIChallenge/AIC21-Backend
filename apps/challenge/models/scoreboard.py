from django.db import models

from model_utils.models import TimeStampedModel


class Scoreboard(TimeStampedModel):
    tournament = models.OneToOneField(
        to='challenge.Tournament',
        on_delete=models.CASCADE,
        related_name='scoreboard'
    )
    freeze = models.BooleanField(default=False)

    def add_scoreboard_row(self, team):
        from apps.challenge.models import ScoreboardRow

        if not self.rows.filter(team=team).exists():
            row = ScoreboardRow.objects.create(
                scoreboard=self,
                team=team,
            )
            return row
        return None

    def get_team_row(self, team):
        return self.rows.get(team=team)
