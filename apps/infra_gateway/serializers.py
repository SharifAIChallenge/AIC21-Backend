from rest_framework import serializers

from apps.challenge.models import Match
from apps.team.models import Submission


class CompiledSubmissionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Submission
        fields = ['infra_compile_message', 'status','infra_compile_token']

class MatchSerializer(serializers.ModelSerializer):

    class Meta:
        model = Match
        fields = ['status','log_file_token']