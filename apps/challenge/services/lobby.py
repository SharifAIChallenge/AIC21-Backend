from apps.challenge.models import LobbyQueue, Map, Match, Tournament
from apps.challenge.models.lobby import LobbyTypes
from apps.challenge.models.tournament import TournamentTypes


class LobbyService:
    @staticmethod
    def run_tournament_after_team_join(lobby_q):
        if lobby_q.get_lobby_population() < lobby_q.get_lobby_size():
            return

        if lobby_q.game_type == LobbyTypes.FRIENDLY_MATCH:
            LobbyService.run_friendly_tournament(lobby_q)

        # TODO : Handle for Mini Tournaments (Level Based)

    @staticmethod
    def run_friendly_tournament(lobby_q):
        records = LobbyQueue.objects.filter(game_type=LobbyTypes.FRIENDLY_MATCH)[:2]
        game_map = Map.objects.filter(actice=True).order_by('?').first()
        friendly_tournament = Tournament.objects.filter(types=TournamentTypes.FRIENDLY).first()

        Match.create_match(records[0].team, records[1].team, friendly_tournament, game_map)

        records.delete()
