from django.conf.urls import url
from django.urls import path
from apps.challenge.views import LobbyAPIView, ScoreboardAPIView, \
    TournamentAPIView, ClanAPIView, LevelBasedTournamentAPIView, LevelBasedTournamentAddTeamsAPIView, RequestAPIView, \
    FriendlyScoreboardAPIView, MatchAPIView

urlpatterns = [
    path('request', view=RequestAPIView.as_view(), name='request'),
    path('request/<int:request_id>', view=RequestAPIView.as_view(), name='request_update'),
    path('lobby', view=LobbyAPIView.as_view(), name='lobby'),
    path('friendly_scoreboard', view=FriendlyScoreboardAPIView.as_view(), name='friendly_scoreboard'),
    path('scoreboard/<int:tournament_id>', view=ScoreboardAPIView.as_view(), name='scoreboard'),
    path('tournament', view=TournamentAPIView.as_view(), name='tournament'),
    path('clan', view=ClanAPIView.as_view(), name='clan'),
    path('match', view=MatchAPIView.as_view(), name='matches'),

    # Level Based Tournaments APIs
    path('level_based_tournament', view=LevelBasedTournamentAPIView.as_view(), name='level_based_tournament'),
    path('level_based_tournament/add_teams', view=LevelBasedTournamentAddTeamsAPIView.as_view(), name='level_based_tournament_add_teams')
]

