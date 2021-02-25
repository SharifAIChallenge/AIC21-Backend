from rest_framework import serializers

from apps.challenge.models import Match


class MatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = ('team1', 'team2', 'status', 'winner', 'log',
                  'tournament', 'is_freeze')

