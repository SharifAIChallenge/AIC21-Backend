from rest_framework import serializers

from apps.challenge.models import LevelBasedTournament


class LevelBasedTournamentSerializer(serializers.ModelSerializer):
    class Meta:
        model = LevelBasedTournament
        fields = ('tournament', 'size')
