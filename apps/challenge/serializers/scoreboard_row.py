from rest_framework import serializers

from apps.challenge.models import ScoreboardRow


class ScoreboardRowSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScoreboardRow
        fields = ('team', 'score', 'wins', 'losses', 'draws')
