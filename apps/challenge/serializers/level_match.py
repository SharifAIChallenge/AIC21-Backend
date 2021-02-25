from rest_framework import serializers

from apps.challenge.models import LevelMatch


class LevelMatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = LevelMatch
        fields = ('match', 'level')
