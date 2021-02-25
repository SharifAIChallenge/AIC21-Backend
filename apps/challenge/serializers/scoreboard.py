from rest_framework import serializers

from apps.challenge.models import Scoreboard


class ScoreboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scoreboard
        fields = ('tournament', 'freeze')
