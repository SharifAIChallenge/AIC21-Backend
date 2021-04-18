from rest_framework import serializers

from apps.challenge.models import Match, MatchStatusTypes
from apps.team.models import Submission, SubmissionStatusTypes
from .models import InfraEventPush, EventStatusCodeTypes


class InfraEventPushSerializer(serializers.ModelSerializer):
    class Meta:
        model = InfraEventPush
        fields = ('title', 'token', 'status_code', 'message_body')

    def create(self, validated_data):
        instance = super().create(validated_data)
        status_code = validated_data.get('status_code')
        message_body = validated_data.get('message_body', '')

        if 100 <= status_code < 200:  # Code compile range
            if status_code == 100:
                Submission.update_submission(
                    infra_token=validated_data.get('token'),
                    status=SubmissionStatusTypes.COMPILED,
                    infra_message=message_body
                )
            elif status_code == 102:
                Submission.update_submission(
                    infra_token=validated_data.get('token'),
                    status=SubmissionStatusTypes.FAILED,
                    infra_message=message_body
                )

        elif 400 <= status_code < 500:  # File transfer range
            pass
        elif 500 <= status_code < 600:  # Match status range
            if status_code == 500:
                Match.update_match(
                    infra_token=validated_data.get('token'),
                    status=MatchStatusTypes.RUNNING
                )
            elif status_code == 504:
                Match.update_match(
                    infra_token=validated_data.get('token'),
                    status=MatchStatusTypes.SUCCESSFUL,
                    message=eval(message_body)
                )
            else:
                Match.update_match(
                    infra_token=validated_data.get('token'),
                    status=MatchStatusTypes.FAILED,
                    stats=message_body
                )

        return instance
