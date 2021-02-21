from django.http import Http404
from django.shortcuts import render

# Create your views here.
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .exceptions import NoTeamException
from .models import Team
from .permissions import HasTeam, NoTeam
from .serializers import TeamSerializer
from rest_framework.parsers import MultiPartParser, FormParser


class TeamAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TeamSerializer
    parser_classes = [MultiPartParser, FormParser]
    queryset = Team.objects.all()

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

    def get(self, request):
        team = request.user.team
        data = self.get_serializer(team).data

        return Response(data)

    def put(self, request):
        team = self.get_serializer(data=request.data, instance=request.user.team, partial=True)
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

        return Response(data={"message": "You left the team"}, status=status.HTTP_200_OK)

    def get_permissions(self):
        new_permissions = self.permission_classes
        if self.request.method in ['PUT', 'GET']:
            new_permissions += [HasTeam]
        if self.request.method == 'POST':
            new_permissions += [NoTeam]

        return [permission() for permission in new_permissions]