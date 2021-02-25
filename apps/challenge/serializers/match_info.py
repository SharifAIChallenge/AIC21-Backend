from rest_framework import serializers

from apps.challenge.models import MatchInfo


class MatchInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MatchInfo
        fields = ('team1_score', 'team2_score', 'match_duration', 'map')
