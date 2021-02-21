from django.urls import path

from apps.team.views import TeamAPIView

app_name = 'team'

urlpatterns = [
    path('', view=TeamAPIView.as_view(), name="team_operations"),
    # path('<str:team_id>', view=TeamAPIView.as_view(), name="get_team"),
]
