from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated

from rest_framework.response import Response
from rest_framework import status

from apps.challenge.models import LobbyQueue, Clan, ClanTeam
from apps.challenge.permissions import HasClan, NoClan
from apps.challenge.serializers import LobbyQueueSerializer
from apps.challenge.serializers.clan import ClanSerializer
from apps.challenge.services.lobby import LobbyService
from apps.team.permissions import HasTeam

from .models import Request, RequestTypes
from .serializers import RequestSerializer


class RequestAPIView(GenericAPIView):
    serializer_class = RequestSerializer
    permission_classes = (HasTeam, IsAuthenticated)
    queryset = Request.objects.all()

    def get(self, request):
        data = self.get_serializer(
            instance=self.get_queryset(),
            many=True
        ).data
        return Response(
            data={'data': data},
            status=status.HTTP_200_OK
        )

    def post(self, request):
        serializer = self.get_serializer(
            data=request.data
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            data={'data': serializer.data},
            status=status.HTTP_200_OK
        )

    def put(self, request):
        pass

    def get_queryset(self):
        source = self.request.query_params.get(
            key='source',
            default=1
        )
        try:
            source = int(source)
        except ValueError:
            source = 1

        request_type = self.request.query_params.get(
            key='type',
            default=None
        )
        queryset = self.queryset

        queryset = (queryset.filter(source_team=self.request.user.team)
                    if source else
                    queryset.filter(target_team=self.request.user.team))

        queryset = (queryset.filter(type=request_type)
                    if request_type else
                    queryset)

        return queryset


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
                'remaining_space': max(0,
                                       population - lobby_q.get_lobby_size())
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


class ScoreboardAPIView(GenericAPIView):
    def get(self, request):
        pass


class TournamentAPIView(GenericAPIView):
    def get(self, request):
        pass


class ClanAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated, HasTeam]
    serializer_class = ClanSerializer
    queryset = Clan.objects.all()

    def get(self, request):
        clan = request.user.team.clan_team.clan
        print(type(clan))
        data = self.get_serializer(clan).data
        return Response(data)

    def post(self, request):
        clan = self.get_serializer(data=request.data)
        clan.is_valid(raise_exception=True)
        clan.save()

        return Response(
            data={
                "data": clan.data
            },
            status=status.HTTP_200_OK
        )

    def put(self, request):
        clan = self.get_serializer(data=request.data,
                                   instance=request.user.team.clan_team.clan, partial=True)
        clan.is_valid(raise_exception=True)
        clan.save()

        return Response(
            data={
                "data": clan.data
            },
            status=status.HTTP_200_OK
        )

    def delete(self, request):
        clan_team = get_object_or_404(ClanTeam,team=request.user.team)
        clan = clan_team.clan
        clan_team.delete()
        if (clan_team.clan.leader == request.user.team):
            clan.delete()

        return Response(
            data={"message": "You left the clan"},
            status=status.HTTP_200_OK
        )
    def get_permissions(self):
        new_permissions = self.permission_classes.copy()
        if self.request.method in ['PUT', 'GET', 'DELETE']:
            new_permissions += [HasClan]
        if self.request.method == 'POST':
            new_permissions += [NoClan]
        return [permission() for permission in new_permissions]
