from rest_framework import serializers
from django.conf import settings

from apps.course.models import *


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['title', 'url']

    def create(self, validated_data):
        return Course.objects.create(**validated_data)
