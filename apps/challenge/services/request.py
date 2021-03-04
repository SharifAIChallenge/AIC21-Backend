from apps.challenge.models import Request


class ClanWarRequest:

    def __init__(self, request, team_request: Request):
        self.request = request
        self.team_request = team_request


class ClanInviteRequest:

    def __init__(self, request, team_request: Request):
        self.request = request
        self.team_request = team_request


class FriendlyMatchRequest:

    def __init__(self, request, team_request: Request):
        self.request = request
        self.team_request = team_request
