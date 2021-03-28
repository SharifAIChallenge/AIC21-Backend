from rest_framework import serializers

from apps.challenge.models import Match, Tournament
from apps.team.models import Team


class MatchTeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['name']


class MathTournamentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tournament
        fields = ['name']


class MatchSerializer(serializers.ModelSerializer):
    team1 = MatchTeamSerializer(read_only=True)
    team2 = MatchTeamSerializer(read_only=True)
    winner = MatchTeamSerializer(read_only=True)

    class Meta:
        model = Match
        fields = ('team1', 'team2', 'status', 'winner', 'log', 'tournament')

