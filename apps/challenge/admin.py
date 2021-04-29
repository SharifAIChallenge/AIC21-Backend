from django.contrib import admin
from django.contrib.admin import ModelAdmin

from import_export.admin import ImportExportModelAdmin

from apps.challenge.models import Tournament, LevelBasedTournament, Map, \
    Scoreboard, ScoreboardRow, Match, MatchInfo, LobbyQueue, League, \
    MergeScoreboards
from .resources import MatchResource


@admin.register(MergeScoreboards)
class MergeScoreboardsAdmin(ModelAdmin):
    list_display = ('id', 'src', 'dest', 'coef', 'cost')
    list_display_links = ('id',)


@admin.register(League)
class LeagueAdmin(ModelAdmin):
    list_display = (
        'id', 'tournament_name', 'start_time', 'match_map', 'total_matches',
        'run')

    list_display_links = ('id',)


@admin.register(Match)
class MatchAdmin(ImportExportModelAdmin):
    list_display = ('id', 'team1', 'team2', 'status', 'winner', 'tournament',
                    'infra_token')
    list_display_links = ('id',)
    list_filter = ('tournament', 'status')
    search_fields = ('infra_token',)
    resource_class = MatchResource


@admin.register(LobbyQueue)
class LobbyQueueAdmin(ModelAdmin):
    pass


@admin.register(MatchInfo)
class MatchInfoAdmin(ModelAdmin):
    pass


@admin.register(Tournament)
class TournamentAdmin(ModelAdmin):
    list_display = ('id', 'name', 'type', 'is_hidden', 'start_time',
                    'end_time')
    list_filter = ('type', 'is_hidden')
    search_fields = ('name',)
    list_editable = ('type', 'is_hidden', 'start_time', 'end_time')


@admin.register(LevelBasedTournament)
class LevelBasedTournamentAdmin(ModelAdmin):
    pass


@admin.register(Map)
class MapAdmin(ModelAdmin):
    list_display = ('id', 'name', 'file', 'active', 'infra_token')
    list_display_links = ('id', 'name')
    list_editable = ('file', 'active')
    list_filter = ('active',)
    search_fields = ('name', 'infra_token')


@admin.register(Scoreboard)
class Scoreboard(ModelAdmin):
    list_display = ('id', 'tournament', 'freeze')
    list_display_links = ('id',)
    list_editable = ('freeze', 'tournament')


@admin.register(ScoreboardRow)
class ScoreboardRow(ModelAdmin):
    list_display = ('id', 'scoreboard', 'team', 'score',
                    'wins', 'losses', 'draws')
    list_display_links = ('id',)

    sortable_by = ('wins', 'losses', 'draws', 'score')
