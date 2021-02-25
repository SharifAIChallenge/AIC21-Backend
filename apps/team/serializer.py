from datetime import datetime, timedelta

from django.conf import settings
from django.utils.timezone import utc
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import Submission


class SubmissionSerializer(ModelSerializer):

    class Meta:
        model = Submission
        fields = ['id', 'language', 'is_final', 'submit_time', 'user', 'file',
                  'download_link', 'status']


class SubmissionPostSerializer(ModelSerializer):
    class Meta:
        model = Submission
        fields = ['language', 'file']

    def validate(self, attrs):
        user = self.context['request'].user

        if not hasattr(user, 'team'):  #check if team is null, user still has that attr or not
            raise serializers.ValidationError(
                'You cant submit, because you dont have a team')
        attrs['user'] = user
        attrs['team'] = user.team
        if attrs['file'].size > Submission.FILE_SIZE_LIMIT:
            raise serializers.ValidationError('File size limit exceeded')
        if not attrs['team'].is_valid: #todo after pulling from arman's branch check this method
            raise serializers.ValidationError('Please complete your team first')

        return attrs

    def save(self, **kwargs):
        instance = super().save(**kwargs)
        instance.handle()
        return instance
