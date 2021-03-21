from django.utils.translation import gettext_lazy as _
# Create your views here.
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.generics import GenericAPIView, get_object_or_404

from apps.accounts.permissions import ProfileComplete
from apps.team.paginations import TeamPagination
from .models import Team, Invitation, Submission
from .permissions import HasTeam, NoTeam
from .serializers import (TeamSerializer, TeamInfoSerializer,
                          UserToTeamInvitationSerializer,
                          TeamToUserInvitationSerializer,
                          UserReceivedInvitationSerializer,
                          TeamPendingInvitationSerializer,
                          SubmissionSerializer, )


class TeamAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TeamSerializer
    parser_classes = [MultiPartParser, FormParser]
    queryset = Team.objects.all()

    def get(self, request):
        team = request.user.team
        data = self.get_serializer(team).data

        return Response(data)

    def post(self, request):
        team = self.get_serializer(data=request.data)
        team.is_valid(raise_exception=True)
        team.save()
        request.user.reject_all_pending_invites()
        return Response(
            data={
                "data": team.data
            },
            status=status.HTTP_200_OK
        )

    def put(self, request):
        team = self.get_serializer(data=request.data,
                                   instance=request.user.team, partial=True)
        team.is_valid(raise_exception=True)
        team.save()

        return Response(
            data={
                "data": team.data
            },
            status=status.HTTP_200_OK
        )

    def delete(self, request):
        current_user = request.user

        if current_user.team.member_count() == 1:
            current_user.team.delete()
        current_user.team = None
        current_user.save()

        return Response(
            data={"message": "You left the team"},
            status=status.HTTP_200_OK
        )

    def get_permissions(self):
        new_permissions = self.permission_classes.copy()
        if self.request.method in ['PUT', 'GET', 'DELETE']:
            new_permissions += [HasTeam]
        if self.request.method == 'POST':
            new_permissions += [NoTeam,ProfileComplete]
        return [permission() for permission in new_permissions]


class TeamSearchAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = TeamSerializer
    pagination_class = TeamPagination
    queryset = Team.objects.all()

    def get(self, request):
        term = request.GET.get('s')
        if term is None or term == '':
            return Response(data={"message": "Provide search parameter"},
                            status=status.HTTP_400_BAD_REQUEST)
        teams = self.get_queryset().filter(name__icontains=term)
        page = self.paginate_queryset(teams)
        results = self.get_serializer(
            page, many=True)

        return self.get_paginated_response(
            data={
                "data": results.data
            }
        )


class TeamInfoAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TeamInfoSerializer
    queryset = Team.objects.all()
    parser_classes = (MultiPartParser, FormParser)

    def get(self, req, team_id):
        team = get_object_or_404(Team, id=team_id)
        data = self.get_serializer(instance=team).data
        return Response(
            data={'data': data},
            status=status.HTTP_200_OK
        )


class IncompleteTeamInfoListAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = TeamInfoSerializer
    pagination_class = TeamPagination
    queryset = Team.objects.all()
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request):
        incomplete_teams_id = [team.id for team in
                               filter(lambda team: not team.is_complete(),
                                      self.get_queryset()
                                      )
                               ]
        incomplete_teams = self.get_queryset().filter(id__in=incomplete_teams_id)
        page = self.paginate_queryset(incomplete_teams)
        data = self.get_serializer(instance=page, many=True).data
        return self.get_paginated_response(
            data={'data': data}
        )

    def get_queryset(self):
        name = self.request.query_params.get('name')

        queryset = self.queryset

        if name:
            queryset = queryset.filter(name__icontains=name)

        return queryset


class UserReceivedPendingInvitationListAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = UserReceivedInvitationSerializer
    queryset = Invitation.objects.all()

    def get(self, request):
        invitations = self.get_queryset().filter(user=request.user,
                                                 status='pending',
                                                 type='team_to_user')
        data = self.get_serializer(instance=invitations, many=True).data
        return Response(
            data={'data': data},
            status=status.HTTP_200_OK
        )


class UserReceivedResolvedInvitationListAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = UserReceivedInvitationSerializer
    queryset = Invitation.objects.all()

    def get(self, request):
        invitations = self.get_queryset().filter(user=request.user,
                                                 type='team_to_user'
                                                 ).exclude(status="pending")
        data = self.get_serializer(instance=invitations, many=True).data
        return Response(
            data={'data': data},
            status=status.HTTP_200_OK
        )


class TeamPendingInvitationListAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated, HasTeam, ]
    serializer_class = TeamPendingInvitationSerializer
    queryset = Invitation.objects.all()

    def get(self, request):
        invitations = self.get_queryset().filter(team=request.user.team,
                                                 status='pending',
                                                 type='user_to_team')
        data = self.get_serializer(instance=invitations, many=True).data
        return Response(
            data={'data': data},
            status=status.HTTP_200_OK
        )


class UserAnswerInvitationAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated, NoTeam]
    serializer_class = UserReceivedInvitationSerializer
    queryset = Invitation.objects.all()

    def put(self, request, invitation_id):
        invitation = get_object_or_404(Invitation, id=invitation_id)
        serializer = self.get_serializer(instance=invitation,
                                         data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        if request.query_params.get('answer') == '1':
            user = invitation.user
            user.team = invitation.team
            invitation.save()
            user.save()
            if (invitation.team.is_complete()):
                invitation.team.reject_all_pending_invitations()
            user.reject_all_pending_invites()

        return Response(
            data={"detail": f"Invitation is {serializer.data['status']}"},
            status=status.HTTP_200_OK
        )

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['invitation_id'] = self.kwargs['invitation_id']
        return context


class TeamAnswerInvitationAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated, HasTeam]
    serializer_class = TeamPendingInvitationSerializer
    queryset = Invitation.objects.all()

    def put(self, request, invitation_id):
        invitation = get_object_or_404(Invitation, id=invitation_id)
        serializer = self.get_serializer(instance=invitation,
                                         data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        if request.query_params.get('answer') == '1':
            print()
            user = invitation.user
            user.team = invitation.team
            user.save()
            if invitation.team.is_complete():
                invitation.team.reject_all_pending_invitations()
            user.reject_all_pending_invites()

        return Response(
            data={"detail": f"Invitation is {serializer.data['status']}"},
            status=status.HTTP_200_OK
        )

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['invitation_id'] = self.kwargs['invitation_id']
        return context


class TeamSentInvitationListAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated, HasTeam, ]
    serializer_class = TeamToUserInvitationSerializer
    queryset = Invitation.objects.all()

    def get(self, request):
        invitations = self.get_queryset().filter(team=request.user.team,
                                                 type='team_to_user')
        data = self.get_serializer(instance=invitations, many=True).data
        return Response(
            data={'data': data},
            status=status.HTTP_200_OK
        )

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            data={"message": "your invitation sent"},
            status=status.HTTP_200_OK
        )


class UserSentInvitationListAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated, NoTeam]
    serializer_class = UserToTeamInvitationSerializer
    queryset = Invitation.objects.all()

    def get(self, request):
        invitations = self.get_queryset().filter(user=request.user,
                                                 type='user_to_team')
        data = self.get_serializer(instance=invitations, many=True).data
        return Response(
            data={'data': data},
            status=status.HTTP_200_OK
        )

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            data={"message": "your invitation sent"},
            status=status.HTTP_200_OK
        )


class SubmissionsListAPIView(GenericAPIView):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer
    permission_classes = (HasTeam,)

    def get(self, request):
        data = self.get_serializer(
            self.get_queryset().filter(team=request.user.team),
            many=True).data
        return Response(data={'submissions': data}, status=status.HTTP_200_OK)


class SubmissionAPIView(GenericAPIView):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer
    permission_classes = (HasTeam,)

    def get(self, request):
        data = self.get_serializer(
            self.get_queryset().filter(team=request.user.team),
            many=True).data
        return Response(data={'submissions': data}, status=status.HTTP_200_OK)

    def post(self, request):
        submission = self.get_serializer(data=request.data,
                                         context={'request': request})
        if submission.is_valid(raise_exception=True):
            submission = submission.save()
            return Response(
                data={'details': _(
                    'Submission information successfully submitted'),
                    'submission_id': submission.id},
                status=status.HTTP_200_OK)
        return Response(data={'errors': [_('Something Went Wrong')]},
                        status=status.HTTP_406_NOT_ACCEPTABLE)

    def put(self, request, submission_id):
        submission = get_object_or_404(Submission, id=submission_id)
        try:
            submission.set_final()
            return Response(
                data={'details': 'Final submission changed successfully'},
                status=status.HTTP_200_OK)
        except ValueError as e:
            return Response(data={'errors': [str(e)]},
                            status=status.HTTP_406_NOT_ACCEPTABLE)
