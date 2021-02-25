from django.conf.urls import url
from django.urls import path
from apps.challenge.views import LobbyAPIView

urlpatterns = [
    path('', view=LobbyAPIView.as_view(), name='lobby'),
]
