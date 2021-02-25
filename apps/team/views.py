from django.utils.translation import ugettext_lazy as _

from rest_framework import status, parsers
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.generics import GenericAPIView, get_object_or_404

from apps.accounts.models import User
from .models import Team, Invitation, Submission
from .permissions import HasTeam, NoTeam
from .serializers import (TeamSerializer, TeamInfoSerializer,
                          UserToTeamInvitationSerializer,
                          TeamToUserInvitationSerializer,
                          UserPendingInvitationSerializer,
                          TeamPendingInvitationSerializer,
                          SubmissionSerializer,)


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
        current_user.team = None
        current_user.save()

        return Response(
            data={"message": "You left the team"},
            status=status.HTTP_200_OK
        )

    def get_permissions(self):
        new_permissions = self.permission_classes
        if self.request.method in ['PUT', 'GET']:
            new_permissions += [HasTeam]
        if self.request.method == 'POST':
            new_permissions += [NoTeam]
        return [permission() for permission in new_permissions]


class TeamSearchAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TeamSerializer
    queryset = Team.objects.all()

    def get(self, request):
        term = request.GET.get('s')
        if term is None or term == '':
            return Response(data={"message": "Provide search parameter"},
                            status=status.HTTP_400_BAD_REQUEST)

        results = self.get_serializer(
            self.get_queryset().filter(name__icontains=term), many=True)

        return Response(
            data={
                "data": results.data
            },
            status=status.HTTP_200_OK
        )


class TeamInfoAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TeamInfoSerializer
    queryset = Team.objects.all()

    def get(self, req, team_id):
        team = get_object_or_404(Team, id=team_id)
        data = self.get_serializer(instance=team).data
        return Response(
            data={'data': data},
            status=status.HTTP_200_OK
        )


class IncompleteTeamInfoListAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TeamInfoSerializer
    queryset = Team.objects.all()

    def get(self, request):
        teams = self.get_queryset()
        teams = filter(lambda team: not team.is_complete(), teams)
        data = self.get_serializer(instance=teams, many=True).data
        return Response(
            data={'data': data},
            status=status.HTTP_200_OK
        )


class UserPendingInvitationListAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserPendingInvitationSerializer
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


class TeamPendingInvitationListAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated, ]
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
    permission_classes = [IsAuthenticated]
    serializer_class = UserPendingInvitationSerializer
    queryset = Invitation.objects.all()

    def put(self, request, invitation_id):
        invitation = self.get_queryset().get(id=invitation_id)
        serializer = self.get_serializer(instance=invitation,
                                         data=request.data)
        serializer.is_valid(raise_exception=True)
        self.validate(request, invitation)
        serializer.save()
        if serializer.data['status'] == 'accepted':
            user = invitation.user
            user.team = invitation.team
            user.save()
            if (invitation.team.is_complete()):
                invitation.team.reject_all_pending_invitations()

        return Response(
            data={"detail": f"Invitation is {request.data['status']}"},
            status=status.HTTP_200_OK
        )

    def validate(self, request, invitation):
        if request.user != invitation.user:
            raise PermissionDenied('this is not your invitation to change')
        elif request.data['status'] == 'rejected' or request.data[
            'status'] == 'pending':
            return True
        elif invitation.team.is_complete():
            raise ValidationError(
                "the team is completed, your invitation is outdated")


class TeamAnswerInvitationAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserPendingInvitationSerializer
    queryset = Invitation.objects.all()

    def put(self, request, invitation_id):
        invitation = self.get_queryset().get(id=invitation_id)
        serializer = self.get_serializer(instance=invitation,
                                         data=request.data)
        serializer.is_valid(raise_exception=True)
        self.validate(request, invitation)
        serializer.save()
        if serializer.data['status'] == 'accepted':
            user = invitation.user
            user.team = invitation.team
            user.save()
            if (invitation.team.is_complete()):
                invitation.team.reject_all_pending_invitations()

        return Response(
            data={"detail": f"Invitation is {request.data['status']}"},
            status=status.HTTP_200_OK
        )

    def validate(self, request, invitation):
        if request.user.team != invitation.team:
            raise PermissionDenied('this is not your invitation to change')
        elif request.data['status'] == 'rejected' or request.data[
            'status'] == 'pending':
            return True
        elif invitation.team.is_complete():
            raise ValidationError("your team is complete")


class TeamSentInvitationListAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = TeamToUserInvitationSerializer
    queryset = Invitation.objects.all()

    def get(self, request):
        invitations = self.get_queryset().filter(team=request.user.team,
                                                 status='team_to_user')
        data = self.get_serializer(instance=invitations, many=True).data
        return Response(
            data={'data': data},
            status=status.HTTP_200_OK
        )

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.validate(request)
        invitation = serializer.save()
        return Response(
            data={"message": "your invitation sent"},
            status=status.HTTP_200_OK
        )

    def validate(self, request):
        target_user = get_object_or_404(User, id=request.data['user'])
        if request.user.team is None:
            raise ValidationError(
                "You have to be in a team to invite other players")
        elif request.user.team.is_complete():
            raise ValidationError(
                'Your team is full, you can not invite anymore player')
        elif target_user.team is not None:
            raise ValidationError('This Player is already in a team')
        elif Invitation.objects.filter(team=request.user.team,
                                       user=request.data['user'],
                                       status='pending').exists():
            raise ValidationError(
                "You have a pending invitation sent for this player")


class UserSentInvitationListAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated, ]
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
        self.validate(request)
        serializer.save()
        return Response(
            data={"message": "your invitation sent"},
            status=status.HTTP_200_OK
        )

    def validate(self, request):
        team = Team.objects.get(id=request.data['team'])
        if request.user.team is not None:
            raise ValidationError(
                "you should leave your team before joining another team")
        elif team.is_complete():
            raise ValidationError('this team is full, you can not join them')
        elif self.get_queryset().filter(team=team, user=request.user,
                                        status='pending').exists():
            raise ValidationError(
                "You have a pending invitation sent for this team")
        return


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
