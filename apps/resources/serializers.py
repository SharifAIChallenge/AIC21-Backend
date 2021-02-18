from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework import serializers
from .models import DownloadLink, Resource


class DownloadLinkSerializer(ModelSerializer):
    class Meta:
        model = DownloadLink
        fields = [
            'url', 'title'
        ]


class ResourceSerializer(ModelSerializer):
    links = DownloadLinkSerializer(many=True)

    class Meta:
        model = Resource
        fields = [
            'title', 'description', 'links'
        ]
