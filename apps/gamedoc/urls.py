from django.urls import path
from apps.gamedoc.views import GamedocAPIView


urlpatterns = [
    path('', view=GamedocAPIView.as_view(), name="Gamedoc"),
]
