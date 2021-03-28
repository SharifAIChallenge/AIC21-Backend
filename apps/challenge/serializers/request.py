from django.shortcuts import get_object_or_404
from rest_framework import serializers

from apps.challenge.exceptions import DuplicatePendingRequestException, SelfRequestException
from apps.challenge.models import Request
from apps.team.exceptions import NoFinalSubmission
from apps.team.models import Team


class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = ('id', 'source_team', 'target_team', 'status', 'type')
        read_only_fields = ('source_team', 'status')

    def create(self, validated_data):
        validated_data['source_team'] = self.context['request'].user.team

        return Request.objects.create(**validated_data)

    def validate(self, data):
        request = self.context['request']
        target_team = get_object_or_404(Team, id=request.data['target_team'])
        if not target_team.has_final_submission():
            raise NoFinalSubmission()
        if target_team == request.user.team:
            raise SelfRequestException()
        elif Request.objects.filter(target_team=target_team,
                                       source_team=request.user.team,
                                       status='pending').exists():
            raise DuplicatePendingRequestException()
        return data