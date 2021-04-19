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
    name = models.CharField(max_length=512, unique=True)
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

    def teams(self):
        from apps.team.models import Team
        team_ids = self.scoreboard.rows.values_list('team_id', flat=True)

        return Team.objects.filter(id__in=team_ids)

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

    def make_league_for_tournament(self, match_map, two_way=False):
        from itertools import combinations

        from apps.challenge.models import Match

        teams = self.teams()
        binaries = list(combinations(list(teams), 2))

        for team1, team2 in binaries:
            Match.create_match(
                team1=team1,
                team2=team2,
                tournament=self,
                match_map=match_map
            )

        if two_way:
            for team2, team1 in binaries:
                Match.create_match(
                    team1=team1,
                    team2=team2,
                    tournament=self,
                    match_map=match_map
                )

        return 2 * len(binaries)

    def __str__(self):
        return f'{self.name}'
