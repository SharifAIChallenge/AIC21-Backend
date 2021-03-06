from django.shortcuts import get_object_or_404
from django.conf import settings

from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied

from apps.accounts.serializer import ProfileSerializer, \
    LimitedProfileSerializer
from apps.challenge.models import Tournament
from .exceptions import NoTeamException, TeamIsFullException, HasTeamException, \
    DuplicatePendingInviteException
from .models import Team, Invitation, Submission
from ..accounts.models import User


class MemberSerializer(serializers.ModelSerializer):
    profile = LimitedProfileSerializer(read_only=True, context={'limited': True})

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'id', 'profile']


class TeamSerializer(serializers.ModelSerializer):
    members = MemberSerializer(many=True, read_only=True)
    creator = MemberSerializer(read_only=True)

    image_url = serializers.SerializerMethodField('_image_url')

    @staticmethod
    def _image_url(obj: Team):
        if not obj.image:
            return ''
        path = obj.image.url
        if settings.DOMAIN not in path:
            return settings.DOMAIN + path
        return path

    class Meta:
        model = Team
        fields = ['name', 'image', 'members', 'creator', 'level_one_payed',
                  'image_url', 'final_payed', 'is_finalist']

    def create(self, data):
        current_user = self.context['request'].user
        data['creator'] = current_user

        team = Team.humans.create(**data)
        friendly_tournament = Tournament.get_friendly_tournament()
        friendly_tournament.scoreboard.add_scoreboard_row(
            team=team
        )

        current_user.team = team
        current_user.save()
        return team

    def validate(self, attrs):
        image = attrs.get('image')

        if image and image.size > Team.IMAGE_MAX_SIZE:
            raise serializers.ValidationError('Maximum file size reached')

        return attrs


class TeamInfoSerializer(serializers.ModelSerializer):
    members = MemberSerializer(many=True, read_only=True)
    creator = MemberSerializer(read_only=True)
    image_url = serializers.SerializerMethodField('_image_url')

    @staticmethod
    def _image_url(obj: Team):
        if not obj.image:
            return ''
        path = obj.image.url
        if settings.DOMAIN not in path:
            return settings.DOMAIN + path
        return path

    class Meta:
        model = Team
        fields = ['name', 'image', 'creator', 'members', 'id', 'image_url']


class UserToTeamInvitationSerializer(serializers.ModelSerializer):
    team = TeamInfoSerializer(read_only=True)

    class Meta:
        model = Invitation
        fields = ['team', 'status', ]

    def create(self, data):
        data['type'] = 'user_to_team'
        current_user = self.context['request'].user
        data['user'] = current_user
        data['team'] = get_object_or_404(Team, id=self.context['request'].data[
            'team_id'])
        invitation = Invitation.objects.create(**data)
        return invitation

    def validate(self, data):
        request = self.context['request']
        team = get_object_or_404(Team,
                                 id=self.context['request'].data['team_id'])
        if team.is_complete():
            raise TeamIsFullException()
        elif Invitation.objects.filter(team=team, user=request.user,
                                       status='pending').exists():
            raise DuplicatePendingInviteException()
        return data


class TeamToUserInvitationSerializer(serializers.ModelSerializer):
    user = MemberSerializer(read_only=True)

    class Meta:
        model = Invitation
        fields = ['user', 'status', ]

    def create(self, data):
        current_user = self.context['request'].user
        data['team'] = current_user.team
        data['type'] = 'team_to_user'
        data['user'] = get_object_or_404(User,
                                         email=self.context['request'].data[
                                             'user_email'])
        invitation = Invitation.objects.create(**data)
        return invitation

    def validate(self, data):
        request = self.context['request']
        # todo: make user_email required
        target_user = get_object_or_404(User, email=request.data['user_email'])
        if request.user.team.is_complete():
            raise TeamIsFullException()
        elif target_user.team is not None:
            raise HasTeamException()
        elif Invitation.objects.filter(team=request.user.team,
                                       user=target_user,
                                       status='pending').exists():
            raise DuplicatePendingInviteException()
        return data


class UserReceivedInvitationSerializer(serializers.ModelSerializer):
    team = TeamInfoSerializer(read_only=True)

    def validate(self, data):
        request = self.context['request']
        invitation = get_object_or_404(Invitation,
                                       id=self.context['invitation_id'])
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
        invitation = get_object_or_404(Invitation,
                                       id=self.context['invitation_id'])

        answer = request.query_params.get('answer', 0)
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
    download_link = serializers.SerializerMethodField('_download_link')

    @staticmethod
    def _download_link(obj: Submission):
        url = obj.file.url
        if settings.DOMAIN not in url:
            return settings.DOMAIN + url
        return url

    class Meta:
        model = Submission
        fields = ['id', 'language', 'file', 'is_final', 'submit_time',
                  'download_link', 'status', 'infra_compile_message',
                  'is_mini_game', 'is_mini_game_final']
        read_only_fields = (
            'id', 'is_final', 'submit_time',
            'user', 'download_link', 'status', 'infra_compile_message',
            'is_mini_game_final'
        )

    def validate(self, attrs):
        from datetime import timedelta
        from django.utils import timezone

        user = self.context['request'].user

        attrs['user'] = user
        attrs['team'] = user.team
        if attrs['file'].size > Submission.FILE_SIZE_LIMIT:
            raise serializers.ValidationError('File size limit exceeded')
        submissions = user.team.submissions.all()
        if submissions.exists() and timezone.now() - \
                submissions.order_by('-submit_time')[
                    0].submit_time < timedelta(
            minutes=5):
            raise serializers.ValidationError(
                f"You have to wait at least "
                f"{10} "
                f"minute between each submission!")

        return attrs

    def save(self, **kwargs):
        instance = super().save(**kwargs)
        instance.handle()
        return instance
