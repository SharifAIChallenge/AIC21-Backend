class LobbyService:
    @staticmethod
    def run_tournament_after_team_join(lobby_q):
        if lobby_q.get_lobby_size != lobby_q.get_lobby_population:
            return
        # TODO : Remove all teams in that queue ( of that type ) and run a tournament