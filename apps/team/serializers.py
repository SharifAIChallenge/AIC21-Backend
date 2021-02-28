from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied

from .exceptions import NoTeamException, TeamIsFullException, HasTeamException, DuplicatePendingInviteException
from .models import Team, Invitation, Submission
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

    def validate(self, data):
        request = self.context['request']

        team = data['team']
        if team.is_complete():
            raise TeamIsFullException()
        elif Invitation.objects.filter(team=team, user=request.user,
                                       status='pending').exists():
            raise DuplicatePendingInviteException()
        return data


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
        target_user = get_object_or_404(User, id=request.data['user'])
        if request.user.team.is_complete():
            raise TeamIsFullException()
        elif target_user.team is not None:
            raise HasTeamException()
        elif Invitation.objects.filter(team=request.user.team, user=target_user, status='pending').exists():
            raise DuplicatePendingInviteException()
        return data


class UserPendingInvitationSerializer(serializers.ModelSerializer):
    team = TeamInfoSerializer(read_only=True)

    def validate(self, data):
        request = self.context['request']
        invitation = get_object_or_404(Invitation, id=self.context['invitation_id'])
        answer = request.query_params.get('answer', "0")

        if request.user != invitation.user:
            raise PermissionDenied('this is not your invitation to change')
        elif answer == '1':
            if invitation.team.is_complete():
                raise TeamIsFullException()
            data['status'] = 'accepted'
        elif answer == '0':
            data['status'] = 'rejected'
        return data

    class Meta:
        model = Invitation
        fields = ['team', 'status', 'id']


class TeamPendingInvitationSerializer(serializers.ModelSerializer):
    user = MemberSerializer(read_only=True)

    def validate(self, data):
        request = self.context['request']
        invitation = get_object_or_404(Invitation, id=self.context['invitation_id'])
        answer = request.query_params.get('answer',0)
        if request.user.team != invitation.team:
            raise PermissionDenied('this is not your invitation to change')
        elif answer == '1':
            if invitation.team.is_complete():
                raise TeamIsFullException()
            data['status'] = 'accepted'
        elif answer == '0':
            data['status'] = 'rejected'
        return data

    class Meta:
        model = Invitation
        fields = ['user', 'status', 'id']


class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = ['language', 'file']
        read_only_fields = (
            'id', 'is_final', 'submit_time',
            'user', 'download_link', 'status'
        )

    def validate(self, attrs):
        user = self.context['request'].user

        attrs['user'] = user
        attrs['team'] = user.team
        if attrs['file'].size > Submission.FILE_SIZE_LIMIT:
            raise serializers.ValidationError('File size limit exceeded')

        return attrs

    def save(self, **kwargs):
        instance = super().save(**kwargs)
        instance.handle()
        return instance
