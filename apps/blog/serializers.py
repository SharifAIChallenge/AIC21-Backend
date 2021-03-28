from rest_framework import serializers
from django.conf import settings

from apps.blog.models import *


class AparatMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = AparatMedia
        fields = ('aparat_id', 'aparat_src')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['name_en', 'name_fa', 'color']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['user', 'text', 'date']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return Comment.objects.create(**validated_data)


class PostSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    aparats = AparatMediaSerializer(many=True, read_only=True)

    num_comments = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['tags', 'num_comments', 'date', 'image',
                  'title_en', 'title_fa', 'text_en', 'text_fa',
                  'description_en', 'description_fa', 'aparats',
                  'google_calendar_link', 'webinar_link', 'is_webinar']

    def get_num_comments(self, obj):
        return obj.comments.count()


class PostDescriptionSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)

    class Meta:
        model = Post
        fields = ['id', 'tags', 'date', 'image', 'title_en',
                  'title_fa', 'description_en', 'description_fa', 'is_webinar']
