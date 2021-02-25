from rest_framework import serializers
from rest_framework.fields import CharField
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


class SubmissionSerializer(ModelSerializer):
    class Meta:
        model = Submission
        fields = ['id', 'language', 'is_final', 'submit_time', 'user', 'file',
                  'download_link', 'status']


class SubmissionPostSerializer(ModelSerializer):
    class Meta:
        model = Submission
        fields = ['language', 'file']

    def validate(self, attrs):
        user = self.context['request'].user

        if not hasattr(user,
                       'team'):  # check if team is null, user still has that attr or not
            raise serializers.ValidationError(
                'You cant submit, because you dont have a team')
        attrs['user'] = user
        attrs['team'] = user.team
        if attrs['file'].size > Submission.FILE_SIZE_LIMIT:
            raise serializers.ValidationError('File size limit exceeded')
        if not attrs[
            'team'].is_valid:  # todo after pulling from arman's branch check this method
            raise serializers.ValidationError(
                'Please complete your team first')

        return attrs

    def save(self, **kwargs):
        instance = super().save(**kwargs)
        instance.handle()
        return instance
