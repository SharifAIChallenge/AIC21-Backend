from rest_framework import serializers

from apps.challenge.models import Clan, ClanTeam
from apps.challenge.serializers.clan_team import ClanTeamSerializer
from apps.team.serializers import TeamSerializer


class ClanSerializer(serializers.ModelSerializer):
    leader = TeamSerializer(read_only=True)
    teams = ClanTeamSerializer(read_only=True,many=True)

    class Meta:
        model = Clan
        fields = (
            'name', 'leader', 'image', 'score', 'wins', 'losses', 'draws','teams'
        )

    def create(self, data):
        current_user = self.context['request'].user
        data['leader'] = current_user.team
        clan = Clan.objects.create(**data)
        self.add_team(clan, current_user.team)
        return clan

    def validate(self, attrs):
        image = attrs.get('image')

        if image and image.size > Clan.IMAGE_MAX_SIZE:
            raise serializers.ValidationError('Maximum file size reached')

        return attrs


    @staticmethod
    def add_team(clan, team):
        clan_team = ClanTeam.objects.create(clan=clan, team=team)
        clan_team.save()
