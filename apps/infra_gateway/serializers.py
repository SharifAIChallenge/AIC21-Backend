from rest_framework import serializers

from apps.team.models import Submission


class CompiledSubmissionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Submission
        fields = ['infra_compile_message', 'status','infra_compile_token']
