from rest_framework import serializers

from apps.challenge.models import Clan, ClanTeam
from apps.team.serializers import TeamSerializer


class ClanTeamSerializer(serializers.ModelSerializer):
    team = TeamSerializer(read_only=True)

    class Meta:
        model = Clan
        fields = (
            'team',
        )