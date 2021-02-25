from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated

from apps.challenge.models import LobbyQueue
from apps.challenge.serializers import LobbyQueueSerializer
from apps.challenge.services.lobby import LobbyService
from apps.team.permissions import HasTeam
from rest_framework.response import Response
from rest_framework import status


class LobbyAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated, HasTeam]
    serializer_class = LobbyQueueSerializer
    queryset = LobbyQueue.objects.all()

    def get(self, request):
        lobby_queues = request.user.team.lobby_queues
        result = []
        for lobby_q in lobby_queues:
            population = lobby_q.get_lobby_population()
            result.append({
                'type': lobby_q.game_type,
                'population': population,
                'remaining_space': max(0, population - lobby_q.get_lobby_size())
            })

        return Response(data={
            'data': result
        }, status=status.HTTP_200_OK)


    def post(self, request):
        lobby_q = self.get_serializer(data=request.data)
        lobby_q.is_valid(raise_exception=True)
        lobby_q.save()

        LobbyService.run_tournament_after_team_join(lobby_q)

        return Response(data="OK", status=status.HTTP_200_OK)
