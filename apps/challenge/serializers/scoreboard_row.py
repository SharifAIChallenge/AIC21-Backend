from rest_framework import serializers

from apps.challenge.models import ScoreboardRow
from apps.team.serializers import TeamInfoSerializer


class ScoreboardRowSerializer(serializers.ModelSerializer):
    team = TeamInfoSerializer(read_only=True)

    class Meta:
        model = ScoreboardRow
        fields = ('team', 'score', 'wins', 'losses', 'draws', 'team_name')
