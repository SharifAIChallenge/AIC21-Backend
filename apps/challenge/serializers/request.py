from rest_framework import serializers

from apps.challenge.models import Request


class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = ('source_team', 'target_team', 'status', 'type')
