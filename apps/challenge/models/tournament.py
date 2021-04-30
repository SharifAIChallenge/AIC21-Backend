from typing import List

from django.db import models
from model_utils.models import TimeStampedModel


class TournamentTypes:
    NORMAL = 'normal'
    FRIENDLY = 'friendly'
    CLANWAR = 'clanwar'
    BOT = 'bot'
    FINAL = 'final'
    TYPES = (
        (NORMAL, 'Normal'),
        (FRIENDLY, 'Friendly'),
        (CLANWAR, 'Clanwar'),
        (BOT, 'Bot'),
        (FINAL, 'Final')
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
    priority = models.IntegerField(default=0)

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
                          is_scoreboard_freeze=False,
                          tournament_type=TournamentTypes.NORMAL):
        from apps.challenge.models import Scoreboard

        if team_list is None:
            team_list = []

        tournament = Tournament.objects.create(
            name=name,
            start_time=start_time,
            end_time=end_time,
            is_hidden=is_hidden,
            type=tournament_type
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
        if two_way:
            return 2 * len(binaries)

        return len(binaries)

    def make_league_multi_maps(self, match_maps, two_way=False):
        total_matches = 0

        for match_map in match_maps:
            total_matches += self.make_league_for_tournament(
                match_map=match_map,
                two_way=two_way
            )
        return total_matches

    def run_next_swiss_round(self, game_maps):
        self.__run_swiss_round(self.scoreboard, game_maps)

    def __run_swiss_round(self, scoreboard, game_maps):
        from apps.team.models import Team
        from apps.challenge.models import Match

        team_ids = self.scoreboard.rows.order_by('-score')
        team_ids = scoreboard.rows.order_by(
            '-score').values_list('team_id', flat=True)

        teams: List[Team] = list(Team.objects.filter(id__in=team_ids))

        bits = [1 for _ in range(0, len(teams))]

        for i, team1 in enumerate(teams):
            if not bits[i]:
                continue
            for j, team2 in enumerate(teams[i + 1:]):
                if bits[j] and not team1.has_match_with_me(team2, self):
                    for map_ in game_maps:
                        Match.create_match(
                            team1=team1,
                            team2=team2,
                            tournament=self,
                            match_map=map_,
                            priority=self.priority
                        )
                    bits[i], bits[j] = 0, 0

                    break

    @staticmethod  # Use with caution!!
    def final_final_final(name, start_time, end_time, is_hidden=False):
        from apps.team.models import Team

        t = Tournament.get_friendly_tournament()
        team_ids = t.scoreboard.rows.values_list('team_id', flat=True)
        teams = Team.objects.filter(id__in=team_ids)
        if teams.count() != 48:
            print(
                f"Bakhti, bayad 48ta bashe vali alan {teams.count()} test :("
            )
            return

        return Tournament.create_tournament(
            name=name,
            start_time=start_time,
            end_time=end_time,
            is_hidden=is_hidden,
            team_list=teams,
            tournament_type='final',
        )

    def init_swiss_league(self, src_tournament: 'Tournament', game_maps):
        self.__run_swiss_round(src_tournament.scoreboard, game_maps)

    def __str__(self):
        return f'{self.name}'
