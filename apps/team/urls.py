from django.urls import path

from apps.team.views import TeamAPIView, TeamLeaveAPIView

app_name = 'team'

urlpatterns = [
    path('', view=TeamAPIView.as_view(), name="create_team"),
    path("leave", view=TeamLeaveAPIView.as_view(), name="leave_team"),
]
