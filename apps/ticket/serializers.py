from rest_framework import serializers
from django.conf import settings

from apps.accounts.models import User
from apps.ticket.models import Ticket, Reply


class TicketUserSerializer(serializers.ModelSerializer):
    first_name = serializers.SerializerMethodField('_first_name')
    last_name = serializers.SerializerMethodField('_last_name')

    @staticmethod
    def _first_name(obj: User):
        return obj.profile.firstname_fa

    @staticmethod
    def _last_name(obj: User):
        return obj.profile.lastname_fa

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class ReplySerializer(serializers.ModelSerializer):
    user = TicketUserSerializer(read_only=True)

    class Meta:
        model = Reply
        fields = ['user', 'text', 'created', 'status', 'id']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return Reply.objects.create(**validated_data)


class TicketSerializer(serializers.ModelSerializer):
    replies = ReplySerializer(many=True, read_only=True)
    author = TicketUserSerializer(read_only=True)
    num_replies = serializers.SerializerMethodField(read_only=True)

    @staticmethod
    def get_num_replies(obj):
        return obj.replies.count()

    class Meta:
        model = Ticket
        fields = ('author', 'replies', 'num_replies', 'created', 'tag', 'id',
                  'title', 'text', 'html', 'status', 'is_public')
        read_only_fields = ('created', 'replies', 'num_replies', 'author')

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        ticket = Ticket.objects.create(**validated_data)
        return ticket
