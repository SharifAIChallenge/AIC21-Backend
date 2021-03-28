from rest_framework import serializers

from apps.challenge.models import ScoreboardRow


class ScoreboardRowSerializer(serializers.ModelSerializer):
    team_name = serializers.SerializerMethodField('_team_name')

    @staticmethod
    def _team_name(obj: ScoreboardRow):
        return obj.team.name

    class Meta:
        model = ScoreboardRow
        fields = ('team', 'score', 'wins', 'losses', 'draws', 'team_name')
