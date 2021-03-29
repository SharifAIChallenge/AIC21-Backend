from django.contrib import admin
from django.contrib.admin import ModelAdmin

# Register your models here.
from apps.challenge.models import Tournament, LevelBasedTournament, Map, \
    Scoreboard, ScoreboardRow, Match, MatchInfo, LobbyQueue


@admin.register(Match)
class MatchAdmin(ModelAdmin):
    pass


@admin.register(LobbyQueue)
class LobbyQueueAdmin(ModelAdmin):
    pass


@admin.register(MatchInfo)
class MatchInfoAdmin(ModelAdmin):
    pass


@admin.register(Tournament)
class TournamentAdmin(ModelAdmin):
    pass


@admin.register(LevelBasedTournament)
class LevelBasedTournamentAdmin(ModelAdmin):
    pass


@admin.register(Map)
class MapAdmin(ModelAdmin):
    pass


@admin.register(Scoreboard)
class Scoreboard(ModelAdmin):
    pass


@admin.register(ScoreboardRow)
class ScoreboardRow(ModelAdmin):
    pass
