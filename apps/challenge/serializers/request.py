from rest_framework import serializers

from apps.challenge.models import Request


class RequestSerializer(serializers.ModelSerializer):
    source_team_name = serializers.SerializerMethodField('_source_team_name')
    target_team_name = serializers.SerializerMethodField('_target_team_name')

    @staticmethod
    def _source_team_name(obj: Request):
        return obj.source_team.name

    @staticmethod
    def _target_team_name(obj: Request):
        return obj.target_team.name

    class Meta:
        model = Request
        fields = ('id', 'source_team', 'target_team', 'status', 'type',
                  'source_team_name', 'target_team_name')
        read_only_fields = ('source_team', 'status', 'source_team_name',
                            'target_team_name')

    def create(self, validated_data):
        validated_data['source_team'] = self.context['request'].user.team

        return Request.objects.create(**validated_data)
