from rest_framework import serializers

from apps.challenge.models import Tournament


class TournamentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tournament
        fields = ('name', 'types', 'start_time', 'end_time', 'is_hidden')
