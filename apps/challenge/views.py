from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from rest_framework.response import Response
from rest_framework import status

from apps.challenge.models import LobbyQueue, RequestStatusTypes, LevelBasedTournament
from apps.challenge.serializers import LobbyQueueSerializer
from apps.challenge.services.lobby import LobbyService
from apps.team.permissions import HasTeam, IsTeamFinalSubmissionCompiled

from .models import Request, RequestTypes
from .serializers import RequestSerializer
from .serializers.level_based_tournament import LevelBasedTournamentCreateSerializer, \
    LevelBasedTournamentAddTeamsSerializer
from .serializers.tournament import LevelBasedTournamentUpdateSerializer


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

    def put(self, request, request_id):
        team_request = get_object_or_404(Request, id=request_id)
        answer = self.request.query_params.get('answer', 1)
        try:
            answer = int(answer)
        except ValueError:
            answer = 1

        if answer == 1:
            team_request.status = RequestStatusTypes.ACCEPTED
            # Call services
        elif answer == 0:
            team_request.status = RequestStatusTypes.REJECTED

        return Response(status=status.HTTP_200_OK)

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
    permission_classes = [IsAuthenticated, HasTeam, IsTeamFinalSubmissionCompiled]
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


class ScoreboardAPIView(GenericAPIView):
    def get(self, request):
        pass


class TournamentAPIView(GenericAPIView):
    def get(self, request):
        pass


class ClanAPIView(GenericAPIView):
    def get(self, request):
        pass

    def post(self, request):
        pass

    def put(self, request):
        pass


class LevelBasedTournamentAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request):
        serializer = LevelBasedTournamentCreateSerializer(
            data=request.data
        )

        serializer.save()

        return Response(data="OK", status=status.HTTP_200_OK)


    def put(self, request):
        level_based_tournament = get_object_or_404(LevelBasedTournament.objects.all(), pk=request.id)

        serializer = LevelBasedTournamentUpdateSerializer(
            data=request,
            instance=level_based_tournament.tournament,
            partial=True
        )

        serializer.save()

        return Response(data="OK", status=status.HTTP_200_OK)
        # TODO : Return the object data if needed


class LevelBasedTournamentAddTeamsAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request):
        serializer = LevelBasedTournamentAddTeamsSerializer(
            data=request.data
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(data="OK", status=status.HTTP_200_OK)


