from django.urls import path

from apps.team.views import TeamListAPIView, TeamLeaveAPIView, TeamInfoAPIView, IncompleteTeamInfoListAPIView, \
    UserPendingInvitationListAPIView, TeamSentInvitationListAPIView, UserAnswerInvitationAPIView, \
    UserSentInvitationListAPIView, TeamPendingInvitationListAPIView, TeamAnswerInvitationAPIView

app_name = 'team'

urlpatterns = [
    path('', view=TeamListAPIView.as_view(), name="teams_list"),
    path("leave", view=TeamLeaveAPIView.as_view(), name="leave_team"),
    path('incomplete', view=IncompleteTeamInfoListAPIView.as_view(), name="get_incomplete_teams"),
    path('invitations/user_pending', view=UserPendingInvitationListAPIView.as_view(),
         name="get_user_pending_invitations"),
    path('invitations/team_pending', view=TeamPendingInvitationListAPIView.as_view(),
         name="get_team_pending_invitations"),
    path('invitations/team_pending/<str:invitation_id>', view=TeamAnswerInvitationAPIView.as_view(),
         name="team_answer_invitation"),
    path('invitations/user_pending/<str:invitation_id>', view=UserAnswerInvitationAPIView.as_view(),
         name="user_answer_invitation"),
    path('invitations/user_sent', view=UserSentInvitationListAPIView.as_view(), name="user_sent_invitation_list"),
    path('invitations/team_sent', view=TeamSentInvitationListAPIView.as_view(), name="team_sent_invitation_list"),
    path('<str:team_id>', view=TeamInfoAPIView.as_view(), name="get_team"),
]
