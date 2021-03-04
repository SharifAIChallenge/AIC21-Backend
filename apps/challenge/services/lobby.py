class LobbyService:
    @staticmethod
    def run_tournament_after_team_join(lobby_q):
        if lobby_q.get_lobby_population() < lobby_q.get_lobby_size():
            return


        # TODO : Remove all teams in that queue ( of that type ) and run a tournament
        # TODO : Using factory design pattern run the tournament