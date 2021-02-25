from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.fields import CharField

from .exceptions import NoTeamException, TeamIsFullException, HasTeamException,DuplicatePendingInviteException
from .models import Team, Invitation
from ..accounts.models import User


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class TeamSerializer(serializers.ModelSerializer):
    members = MemberSerializer(many=True, read_only=True)
    creator = MemberSerializer(read_only=True)

    class Meta:
        model = Team
        fields = ['name', 'image', 'members', 'creator']

    def create(self, data):
        current_user = self.context['request'].user
        data['creator'] = current_user

        team = Team.objects.create(**data)
        current_user.team = team
        current_user.save()
        return team


class TeamInfoSerializer(serializers.ModelSerializer):
    members = MemberSerializer(many=True, read_only=True)
    creator = MemberSerializer(read_only=True)

    class Meta:
        model = Team
        fields = ['name', 'image', 'creator', 'members', 'id']


class UserToTeamInvitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invitation
        fields = ['team', 'status']

    def create(self, data):
        data['type'] = 'user_to_team'
        current_user = self.context['request'].user
        data['user'] = current_user
        invitation = Invitation.objects.create(**data)
        return invitation


class TeamToUserInvitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invitation
        fields = ['user', 'status']
        extra_kwargs = {'user': {'required': True}}

    def create(self, data):
        current_user = self.context['request'].user
        data['team'] = current_user.team
        data['type'] = 'team_to_user'
        invitation = Invitation.objects.create(**data)
        return invitation

    def validate(self, data):
        request = self.context['request']
        target_user = get_object_or_404(User, id=data['user'])
        if request.user.team is None:
            raise NoTeamException()
        elif request.user.team.is_complete():
            raise TeamIsFullException()
        elif target_user.team is not None:
            raise HasTeamException()
        elif Invitation.objects.filter(team=request.user.team, user=data['user'], status='pending').exists():
            raise DuplicatePendingInviteException()


class UserPendingInvitationSerializer(serializers.ModelSerializer):
    team = TeamInfoSerializer(read_only=True)

    def validate(self, data):
        # todo: find better way to check status required
        try:
            data['status'] != None
        except:
            raise serializers.ValidationError('status field is required')
        return data

    class Meta:
        model = Invitation
        fields = ['team', 'status', 'id']


class TeamPendingInvitationSerializer(serializers.ModelSerializer):
    user = MemberSerializer(read_only=True)

    def validate(self, data):
        # todo: find better way to check status required
        try:
            data['status'] != None
        except:
            raise serializers.ValidationError('status field is required')
        return data

    class Meta:
        model = Invitation
        fields = ['user', 'status', 'id']
