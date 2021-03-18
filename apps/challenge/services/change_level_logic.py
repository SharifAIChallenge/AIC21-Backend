from apps.challenge.models import LevelBasedTournament, Match, Level, Map
from apps.team.models import Team


class ChangeLevelLogic:

    def __init__(self, tournament: LevelBasedTournament, match_map=None):
        self.tournament = tournament
        self.match_map = match_map if match_map else Map.get_random_map()
        self.last_level = self.tournament.last_level

    def one_deletion_mode(self):
        winner_teams = self.last_level.level_matches.sort_by(
            'id'
        ).values_list(
            'match__winner',
            flat=True
        )
        winner_teams = Team.objects.filter(id__in=winner_teams)

        matches = Match.create_match_from_list(
            teams=winner_teams,
            tournament=self.tournament.tournament,
            match_map=self.match_map
        )
        level = Level.create_level(
            matches=matches,
            tournament=self.tournament,
            last_level=self.last_level
        )

        return level

    def swiss_league_mode(self):
        pass
