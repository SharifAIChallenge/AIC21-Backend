from django.contrib import admin
from django.contrib.admin import ModelAdmin

# Register your models here.
from apps.challenge.models import Tournament, LevelBasedTournament, Map, Scoreboard, ScoreboardRow


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
