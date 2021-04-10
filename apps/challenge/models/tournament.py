from django.db import models
from model_utils.models import TimeStampedModel


class TournamentTypes:
    NORMAL = 'normal'
    FRIENDLY = 'friendly'
    CLANWAR = 'clanwar'
    BOT = 'bot'
    TYPES = (
        (NORMAL, 'Normal'),
        (FRIENDLY, 'Friendly'),
        (CLANWAR, 'Clanwar'),
        (BOT, 'Bot')
    )


class Tournament(TimeStampedModel):
    name = models.CharField(max_length=512)
    type = models.CharField(
        max_length=50,
        choices=TournamentTypes.TYPES,
        default=TournamentTypes.NORMAL
    )
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    is_hidden = models.BooleanField(default=False)

    @staticmethod
    def get_friendly_tournament():
        return Tournament.objects.filter(
            type=TournamentTypes.FRIENDLY).first()

    @staticmethod
    def get_bot_tournament():
        return Tournament.objects.filter(
            type=TournamentTypes.BOT
        ).first()

    @staticmethod
    def create_tournament(name, start_time, end_time, is_hidden,
                          is_friendly=False, team_list=None,
                          is_scoreboard_freeze=False):
        from apps.challenge.models import Scoreboard

        if team_list is None:
            team_list = []

        tournament = Tournament.objects.create(
            name=name,
            start_time=start_time,
            end_time=end_time,
            is_hidden=is_hidden,
            type=TournamentTypes.NORMAL
            if not is_friendly else TournamentTypes.FRIENDLY
        )
        scoreboard = Scoreboard.objects.create(
            tournament=tournament,
            freeze=is_scoreboard_freeze
        )
        for team in team_list:
            scoreboard.add_scoreboard_row(
                team=team
            )

        return tournament

    def reset_scoreboard(self):
        from apps.challenge.models import MatchStatusTypes

        self.scoreboard.rows.update(score=1000)
        self.scoreboard.rows.update(wins=0)
        self.scoreboard.rows.update(losses=0)
        self.scoreboard.rows.update(draws=0)

        matches = self.matches.filter(
            status=MatchStatusTypes.SUCCESSFUL).order_by(
            'id')

        for match in matches:
            match.update_score()

    def __str__(self):
        return f'{self.name}'
