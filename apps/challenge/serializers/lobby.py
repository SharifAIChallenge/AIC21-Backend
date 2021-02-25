from rest_framework import serializers

from apps.challenge.models import LobbyQueue
from apps.challenge.models.lobby import LobbyTypes


class LobbyQueueSerializer(serializers.ModelSerializer):
    class Meta:
        model = LobbyQueue
        fields = ['game_type']

    def validate(self, data):
        if data['game_type'] not in LobbyTypes.TYPES_ARR:
            raise serializers.ValidationError(
                'Invalid lobby type. it should be one of ' + ", ".join(LobbyTypes.TYPES_ARR)
            )

        return data

    def create(self, data):
        data['team'] = self.context['request'].user.team
        team = LobbyQueue.objects.create(**data)

        return team

