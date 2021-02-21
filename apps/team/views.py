from django.http import Http404
from django.shortcuts import render

# Create your views here.
from rest_framework.exceptions import  PermissionDenied, ValidationError
from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from apps.accounts.models import User
from .models import Team, Invitation
from .serializers import TeamSerializer, TeamInfoSerializer, UserToTeamInvitationSerializer, \
    TeamToUserInvitationSerializer, UserPendingInvitationSerializer
from rest_framework.parsers import MultiPartParser, FormParser


class TeamListAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TeamSerializer
    parser_classes = [MultiPartParser, FormParser]
    queryset = Team.objects.all()

    def get(self, request):
        teams = self.get_queryset()
        data = self.get_serializer(instance=teams, many=True).data
        return Response(
            data={'data': data},
            status=status.HTTP_200_OK
        )

    def post(self, request):
        team = self.get_serializer(data=request.data)
        team.is_valid(raise_exception=True)
        team.save()

        return Response(
            data={"message": "Team created successfully"},
            status=status.HTTP_200_OK
        )


class TeamLeaveAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        current_user = request.user
        current_user.team = None
        current_user.save()

        return Response(
            data={"message": "You left the team"},
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
        invitations = self.get_queryset().filter(target_user=request.user, status='pending', type='team_to_user')
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
        serializer = self.get_serializer(instance=invitation, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.validate(request.data, invitation,request.user)
        serializer.save()
        if serializer.data['status'] == 'accepted':
            target_user = invitation.target_user
            target_user.team = invitation.team
            target_user.save()

        return Response(
            data={"detail": f"Invitation is {request.data['status']}"},
            status=status.HTTP_200_OK
        )

    def validate(self, data, invitation,user):
        if user != invitation.target_user:
            raise PermissionDenied('this is not your invitation to change')
        elif data['status'] == 'rejected' or data['status'] == 'pending':
            return
        elif invitation.team.is_complete():
            raise ValidationError("the team is completed, your invitation is outdated")



class TeamSentInvitationListAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TeamToUserInvitationSerializer
    queryset = Invitation.objects.all()

    def get(self, request):
        invitations = request.user.team.invitations
        data = self.get_serializer(instance=invitations, many=True).data
        return Response(
            data={'data': data},
            status=status.HTTP_200_OK
        )

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.validate(serializer.data, request.user)
        invitation = serializer.save()
        return Response(
            data={"message": "your invitation sent"},
            status=status.HTTP_200_OK
        )

    def validate(self, data, user):
        if user.team is None:
            raise ValidationError("You have to be in a team to invite other players")
        if user.team.is_complete():
            raise ValidationError('Your team is full, you can not invite anymore player')
        if Invitation.objects.filter(team=user.team, target_user=data['target_user'], status='pending').exists():
            raise ValidationError("You have a pending invitation for this player")

# class UserSentInvitationListAPIView