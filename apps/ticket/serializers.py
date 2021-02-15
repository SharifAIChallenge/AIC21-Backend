from rest_framework import serializers
from django.conf import settings

from apps.ticket.models import Ticket, Reply


class ReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = Reply
        fields = ['user', 'text', 'date']

    def create(self, validated_data):
        validated_data['user'] = self.request.user
        return Reply.objects.create(**validated_data)


class TicketSerializer(serializers.ModelSerializer):
    replies = ReplySerializer(many=True)
    num_replies = serializers.SerializerMethodField()

    class Meta:
        model = Ticket
        fields = ['replies', 'num_replies', 'date', 'image',
                  'title', 'author', 'text']

    def get_num_replies(self, obj):
        return obj.replies.count()
