from django.http import Http404
from django.shortcuts import render

# Create your views here.
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import Team
from .serializers import TeamSerializer, TeamInfoSerializer
from rest_framework.parsers import MultiPartParser, FormParser


class TeamAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TeamSerializer
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        team = self.get_serializer(data=request.data)
        team.is_valid(raise_exception=True)
        team.save()

        return Response(
            data={
                "message": "Team created successfully"
            },
            status=status.HTTP_200_OK
        )

class TeamLeaveAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        current_user = request.user
        current_user.team = None
        current_user.save()

        return Response(data={"message": "You left the team"}, status=status.HTTP_200_OK)


class TeamInfoAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TeamInfoSerializer
    queryset = Team.objects.all()

    def get(self, req, team_id):
        try:
            data = self.get_serializer(self.get_queryset().get(pk=team_id)).data
            return Response(data)
        except Team.DoesNotExist:
            raise Http404