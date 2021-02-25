from django.conf.urls import url
from django.urls import path
from apps.challenge.views import LobbyAPIView, ScoreboardAPIView, TournamentAPIView, ClanAPIView

urlpatterns = [
    path('lobby', view=LobbyAPIView.as_view(), name='lobby'),
    path('scoreboard', view=ScoreboardAPIView.as_view(), name='scoreboard'),
    path('tournament', view=TournamentAPIView.as_view(), name='tournament'),
    path('clan', view=ClanAPIView.as_view(), name='clan'),
]
