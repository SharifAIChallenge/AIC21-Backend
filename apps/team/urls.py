from django.urls import path

from apps.team.views import TeamListAPIView, TeamLeaveAPIView, TeamInfoAPIView, IncompleteTeamInfoListAPIView

app_name = 'team'

urlpatterns = [
    path('', view=TeamListAPIView.as_view(), name="create_team"),
    path("leave", view=TeamLeaveAPIView.as_view(), name="leave_team"),
    path('incomplete', view=IncompleteTeamInfoListAPIView.as_view(),name = "get_incomplete_teams"),
    path('<str:team_id>', view=TeamInfoAPIView.as_view(), name="get_team"),
]
