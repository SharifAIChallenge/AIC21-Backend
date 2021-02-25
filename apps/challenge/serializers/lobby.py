from rest_framework import serializers

from apps.challenge.models import LobbyQueue


class LobbyQueueSerializer(serializers.ModelSerializer):
    class Meta:
        model = LobbyQueue
        fields = ('team', 'game_type')
