from apps.challenge.models import LevelBasedTournament, Match, Level


class ChangeLevelLogic:

    def __init__(self, tournament: LevelBasedTournament):
        self.tournament = tournament

    def one_deletion(self):
        winner_teams = self.tournament.last_level.level_matches.sort_by(
            'id'
        ).values_list(
            'match__winner'
        )
        matches = ...
