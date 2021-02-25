from rest_framework import serializers

from apps.challenge.models import ClanWar


class ClanWarSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClanWar
        fields = ('clan1', 'clan2', 'tournament')
