from django.urls import path

from apps.team.views import TeamAPIView

app_name = 'team'

urlpatterns = [
    path('', view=TeamAPIView.as_view(), name="create_team"),
]
