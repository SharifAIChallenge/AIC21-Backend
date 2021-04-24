from django.db.models import Q
from django.utils import timezone

from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from rest_framework.response import Response
from rest_framework import status

from apps.challenge.models import LobbyQueue, RequestStatusTypes, \
    LevelBasedTournament, Match, Scoreboard, ScoreboardRow, Tournament, \
    MatchStatusTypes
from apps.challenge.models.tournament import TournamentTypes
from apps.challenge.serializers import LobbyQueueSerializer, \
    ScoreboardSerializer, ScoreboardRowSerializer, \
    MatchSerializer, TournamentSerializer
from apps.challenge.services.lobby import LobbyService
from apps.paginations import MatchPagination
from apps.team.models import Team
from apps.team.permissions import HasTeam, TeamHasFinalSubmission

from .models import Request, RequestTypes
from .serializers import RequestSerializer
from .serializers.level_based_tournament import \
    LevelBasedTournamentCreateSerializer, \
    LevelBasedTournamentAddTeamsSerializer
from .serializers.tournament import LevelBasedTournamentUpdateSerializer
from ..paginations import ScoreboardRowPagination
from django.db.models import Q


class RequestAPIView(GenericAPIView):
    serializer_class = RequestSerializer
    permission_classes = (IsAuthenticated, HasTeam, TeamHasFinalSubmission)
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
        team_request = get_object_or_404(
            Request,
            id=request_id,
            target_team=request.user.team,
            status=RequestStatusTypes.PENDING
        )
        answer = self.request.query_params.get('answer', 1)
        try:
            answer = int(answer)
        except ValueError:
            answer = 1

        if answer == 1:
            team_request.status = RequestStatusTypes.ACCEPTED
            if team_request.type == RequestTypes.FRIENDLY_MATCH:
                Match.create_friendly_match(
                    team1=team_request.source_team,
                    team2=team_request.target_team,
                )
        elif answer == 0:
            team_request.status = RequestStatusTypes.REJECTED

        team_request.save()

        return Response(
            data={"status": True},
            status=status.HTTP_200_OK
        )

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
    permission_classes = [IsAuthenticated, HasTeam, TeamHasFinalSubmission]
    serializer_class = LobbyQueueSerializer
    queryset = LobbyQueue.objects.all()

    def get(self, request):
        # Such a shit :| ... do this with serializer later
        # lobby_queues = self.get_queryset()
        # user_lobby_queues = request.user.team.lobby_queues.all()
        # result = []
        # for lobby_q in lobby_queues:
        #     population = lobby_q.get_lobby_population()
        #     result.append({
        #         'type': lobby_q.game_type,
        #         'population': population,
        #         'remaining_space': max(0,
        #                                lobby_q.get_lobby_size() - population),
        #         'is_joined': lobby_q in user_lobby_queues,
        #     })

        lobby_queues = request.user.team.lobby_queues.all()
        data = self.get_serializer(
            instance=lobby_queues,
            many=True
        ).data

        return Response(data={
            'data': data
        }, status=status.HTTP_200_OK)

    def post(self, request):
        lobby_q = self.get_serializer(data=request.data)
        lobby_q.is_valid(raise_exception=True)
        lobby_queue = lobby_q.save()

        LobbyService.run_tournament_after_team_join(lobby_queue)

        return Response(data={"status": True}, status=status.HTTP_200_OK)


class ScoreboardAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ScoreboardRowSerializer
    pagination_class = ScoreboardRowPagination
    queryset = ScoreboardRow.objects.all()

    def get(self, request, tournament_id):
        scoreboard_rows = self.get_corrected_queryset(tournament_id)
        page = self.paginate_queryset(scoreboard_rows)
        data = self.get_serializer(instance=page, many=True).data

        return self.get_paginated_response(
            data={'data': data}
        )

    def get_corrected_queryset(self, tournament_id):
        no_match_teams = ScoreboardRow.objects.filter(
            scoreboard__tournament_id=tournament_id).filter(
            wins=0
        ).filter(losses=0).filter(draws=0).values_list('id', flat=True)

        has_match_teams = ScoreboardRow.objects.exclude(
            id__in=no_match_teams).filter(
            scoreboard__tournament_id=tournament_id).order_by('-score')
        no_match_teams = ScoreboardRow.objects.filter(id__in=no_match_teams)

        return list(has_match_teams) + list(no_match_teams)


class FriendlyScoreboardAPIView(GenericAPIView):
    def get(self, request):
        return ScoreboardAPIView.as_view()(request._request,
                                           Tournament.get_friendly_tournament().id)


class TournamentAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = TournamentSerializer
    queryset = Tournament.objects.filter(
        type__in=[TournamentTypes.NORMAL, TournamentTypes.FINAL]).exclude(
        start_time=None
    ).filter(is_hidden=False)

    def get(self, request):
        curr_time = timezone.now()
        queryset = self.get_queryset().order_by('id')
        data = self.get_serializer(queryset, many=True).data

        return Response(
            data={'data': data},
            status=status.HTTP_200_OK
        )


class NextTournamentAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated, HasTeam)
    serializer_class = TournamentSerializer

    def get(self, request):
        curr_time = timezone.now()
        tournament = Tournament.objects.filter(
            type=TournamentTypes.NORMAL
        ).exclude(start_time=None).filter(
            start_time__gt=curr_time
        ).order_by('start_time').first()

        data = self.get_serializer(tournament).data

        return Response(
            data={'data': data},
            status=status.HTTP_200_OK
        )


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
        level_based_tournament = get_object_or_404(
            LevelBasedTournament.objects.all(), pk=request.id)

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


class MatchAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated, HasTeam]
    serializer_class = MatchSerializer
    queryset = Match.objects.all()

    pagination_class = MatchPagination

    def get(self, request):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)

        data = self.get_serializer(
            instance=page,
            many=True
        ).data

        return self.get_paginated_response(
            data={'data': data},
        )

    def get_queryset(self):
        match_status = self.request.query_params.get('status')

        tournament_id = self.request.query_params.get(
            'tournament_id',
        )
        try:
            tournament_id = int(tournament_id)
        except TypeError:
            tournament_id = None

        if not tournament_id:
            queryset = self.queryset.exclude(
                tournament__type=TournamentTypes.NORMAL)
        else:
            queryset = self.queryset.filter(
                tournament_id=tournament_id
            )

        queryset = queryset.filter(
            Q(team1=self.request.user.team) | Q(team2=self.request.user.team)
        )

        if match_status:
            queryset = queryset.filter(
                status=match_status

            )

        return queryset.order_by('-id')


class BotAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated, HasTeam)

    def get(self, request):
        next_bot = Team.get_next_level_bot(request.user.team)
        if next_bot is None:
            next_bot = Team.bots.all().order_by('bot_number').last()
        opened_bots = Team.bots.filter(bot_number__lte=next_bot.bot_number)

        data = [{'number': bot.bot_number, 'name': bot.name} for bot in
                opened_bots]

        return Response(
            data={'data': data},
            status=status.HTTP_200_OK
        )

    def post(self, request, bot_number):
        next_bot = Team.get_next_level_bot(request.user.team)
        if next_bot is None:
            next_bot = Team.bots.all().order_by('bot_number').last()
        if bot_number < 1 or bot_number > next_bot.bot_number:
            return Response(status=status.HTTP_403_FORBIDDEN)

        bot = Team.bots.get(bot_number=bot_number)

        Match.create_bot_match(bot, request.user.team)

        return Response(
            status=status.HTTP_200_OK
        )


class TeamsWonBotAPIView(GenericAPIView):

    def get(self, request):
        bots = Team.bots.all()
        data = {}

        for bot in bots:
            team_ids = bot.rival_teams_wins()
            teams = Team.humans.filter(
                id__in=team_ids).values_list('name', flat=True)

            data[bot.name] = list(teams)

        return Response(
            data={'data': data},
            status=status.HTTP_200_OK
        )
