from rest_framework import serializers
from .models import Team
from ..accounts.models import User


class TeamSerializer(serializers.ModelSerializer):

    class Meta:
        model = Team
        fields = ['name', 'image','id']

    def validate(self, data):
        user = self.context['request'].user
        if user.team is not None:
            raise serializers.ValidationError('You have to leave your current team first, then you can create a team')

        return data

    def create(self, data):
        current_user = self.context['request'].user
        data['creator'] = current_user

        team = Team.objects.create(**data)
        current_user.team = team
        current_user.save()
        return team


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class TeamInfoSerializer(serializers.ModelSerializer):
    members = MemberSerializer(many=True, read_only=True)
    creator = MemberSerializer(read_only=True)

    class Meta:
        model = Team
        fields = ['name', 'image', 'creator', 'members']
