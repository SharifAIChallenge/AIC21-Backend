from rest_framework import serializers
from rest_framework.fields import CharField

from .models import Team, Invitation
from ..accounts.models import User


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['name', 'image', 'id']

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


class UserToTeamInvitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invitation
        fields = ['team', 'status']

    def create(self, data):
        data['type'] = 'user_to_team'
        invitation = Invitation.objects.create(**data)
        return invitation


class TeamToUserInvitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invitation
        fields = ['target_user', 'status']
        extra_kwargs = {'target_user': {'required': True}}


    def create(self, data):
        current_user = self.context['request'].user
        data['team'] = current_user.team
        data['type'] = 'team_to_user'
        invitation = Invitation.objects.create(**data)
        return invitation


class UserPendingInvitationSerializer(serializers.ModelSerializer):
    team = TeamInfoSerializer(read_only=True)

    def validate(self, data):
        try:
            data['status'] != None
        except:
            raise serializers.ValidationError('status field is required')
        return data

    class Meta:
        model = Invitation
        fields = ['team', 'status', 'id']
