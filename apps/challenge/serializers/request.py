from rest_framework import serializers

from apps.challenge.models import Request


class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = ('id', 'source_team', 'target_team', 'status', 'type')
        read_only_fields = ('source_team', 'status')

    def create(self, validated_data):
        validated_data['source_team'] = self.context['request'].user.team

        return Request.objects.create(**validated_data)
