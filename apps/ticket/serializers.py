from rest_framework import serializers
from django.conf import settings

from apps.ticket.models import Ticket, Reply


class ReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = Reply
        fields = ['user','text', 'created']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return Reply.objects.create(**validated_data)


class TicketSerializer(serializers.ModelSerializer):
    replies = ReplySerializer(many=True, read_only=True)
    num_replies = serializers.SerializerMethodField()

    @staticmethod
    def get_num_replies(obj):
        return obj.replies.count()

    class Meta:
        model = Ticket
        fields = ('replies', 'num_replies', 'created', 'tag','id',
                  'title', 'text', 'html')
        read_only_fields = ('created', 'replies', 'num_replies')

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        ticket = Ticket.objects.create(**validated_data)
        return ticket
