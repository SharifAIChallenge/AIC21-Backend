from rest_framework import serializers
from django.conf import settings

from apps.accounts.models import User
from apps.accounts.serializer import ProfileSerializer
from apps.ticket.models import Ticket, Reply, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'title')


class TicketUserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True, context={'limited': True})

    class Meta:
        model = User
        fields = ('email', 'profile')


class ReplySerializer(serializers.ModelSerializer):
    user = TicketUserSerializer(read_only=True)
    is_owner = serializers.SerializerMethodField('_is_owner')

    def _is_owner(self, obj: Reply):
        return obj.user.id == self.context['request'].user.id

    class Meta:
        model = Reply
        fields = ['user', 'text', 'created', 'status', 'id', 'is_owner']
        read_only_fields = ('user', 'status', 'created', 'id', 'is_owner')

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        validated_data['ticket_id'] = self.context['ticket_id']

        return Reply.objects.create(**validated_data)


class LimitedTicketSerializer(serializers.ModelSerializer):
    num_replies = serializers.SerializerMethodField(read_only=True)

    @staticmethod
    def get_num_replies(obj):
        return obj.replies.count()

    class Meta:
        model = Ticket
        fields = ('num_replies', 'created', 'tag', 'id',
                  'title', 'status', 'is_public')
        read_only_fields = ('created', 'replies', 'num_replies', 'author')

    def to_representation(self, instance: Ticket):
        data = super().to_representation(instance)
        data['tag'] = TagSerializer(
            instance=instance.tag
        ).data

        return data


class TicketSerializer(serializers.ModelSerializer):
    author = TicketUserSerializer(read_only=True)
    num_replies = serializers.SerializerMethodField(read_only=True)

    @staticmethod
    def get_num_replies(obj):
        return obj.replies.count()

    class Meta:
        model = Ticket
        fields = ('author', 'num_replies', 'created', 'tag', 'id',
                  'title', 'text', 'status', 'is_public')
        read_only_fields = ('created', 'num_replies', 'author')

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        ticket = Ticket.objects.create(**validated_data)
        return ticket

    def to_representation(self, instance: Ticket):
        data = super().to_representation(instance)

        replies = instance.replies.all().order_by('created')
        data['replies'] = ReplySerializer(
            instance=replies,
            many=True,
            context={'request': self.context['request']}
        ).data

        data['tag'] = TagSerializer(
            instance=instance.tag
        ).data

        return data
