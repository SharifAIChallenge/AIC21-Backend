from rest_framework import serializers

from apps.challenge.models import Tournament


class TournamentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tournament
        fields = ('name', 'types', 'start_time', 'end_time', 'is_hidden')


class LevelBasedTournamentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tournament
        fields = ('name', 'start_time', 'end_time', 'is_hidden',
                  'is_friendly', 'is_scoreboard_freeze')

