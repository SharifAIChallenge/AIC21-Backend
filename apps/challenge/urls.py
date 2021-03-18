from django.conf.urls import url
from django.urls import path
from apps.challenge.views import LobbyAPIView, ScoreboardAPIView, \
    TournamentAPIView, ClanAPIView, LevelBasedTournamentAPIView

urlpatterns = [
    path('lobby', view=LobbyAPIView.as_view(), name='lobby'),
    path('scoreboard', view=ScoreboardAPIView.as_view(), name='scoreboard'),
    path('tournament', view=TournamentAPIView.as_view(), name='tournament'),
    path('clan', view=ClanAPIView.as_view(), name='clan'),

    # Level Based Tournaments APIs
    path('level_based_tournament', view=LevelBasedTournamentAPIView.as_view(), name='level_based_tournament')
]
