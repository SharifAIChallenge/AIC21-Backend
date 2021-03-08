from django.utils.translation import gettext_lazy as _

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueValidator

from .models import User, Profile, ResetPasswordToken, Skill, JobExperience


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ('skill',)

    def create(self, validated_data):
        validated_data['profile'] = self.context['request'].user.profile

        return Skill.objects.create(**validated_data)


class JobExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobExperience
        fields = ('company', 'position', 'description')

    def create(self, validated_data):
        validated_data['profile'] = self.context['request'].user.profile

        return JobExperience.objects.create(**validated_data)


class ProfileSerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True)
    jobs = JobExperienceSerializer(many=True)
    is_complete = serializers.SerializerMethodField('_is_complete')

    @staticmethod
    def _is_complete(obj: Profile):
        return obj.is_complete

    class Meta:
        model = Profile
        exclude = ['user', 'id']

    def validate(self, attrs):
        image = attrs.get('image')

        if image and image.size > Profile.IMAGE_MAX_SIZE:
            raise serializers.ValidationError('Maximum file size reached')

        return attrs


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)

    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password_1 = serializers.CharField(
        style={'input_type': 'password'}
    )
    password_2 = serializers.CharField(
        style={'input_type': 'password'}
    )

    class Meta:
        model = User
        fields = ['email', 'password_1', 'password_2', 'profile']

    def validate(self, attrs):
        if attrs.get('password_1') != attrs.get('password_2'):
            raise ValidationError(_("Passwords not match"))

        return attrs

    def create(self, validated_data):
        validated_data.pop('password_2')
        validated_data['password'] = validated_data.pop('password_1')

        user = User.objects.create_user(
            username=validated_data.get('email'),
            email=validated_data.get('email'),
            password=validated_data.get('password'),
            is_active=False
        )
        profile = Profile.objects.create(user=user)

        return user


class ResetPasswordConfirmSerializer(serializers.ModelSerializer):
    new_password1 = serializers.CharField(max_length=100)
    new_password2 = serializers.CharField(max_length=100)

    class Meta:
        model = ResetPasswordToken
        fields = ['new_password1', 'new_password2', 'uid', 'token']

    def validate(self, data):
        if data['new_password1'] != data['new_password2']:
            raise serializers.ValidationError('passwords don\'t match!')
        return data


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(style={'input_type': 'password'})
    new_password1 = serializers.CharField(style={'input_type': 'password'})
    new_password2 = serializers.CharField(style={'input_type': 'password'})

    def validate(self, data):
        if data['new_password1'] != data['new_password2']:
            raise serializers.ValidationError(_('passwords don\'t match!'))
        if not self.context['request'].user.check_password(
                data['old_password']):
            raise serializers.ValidationError(_('invalid old password'))
        return data

    def save(self, **kwargs):
        user = self.context['request'].user
        user.set_password(
            raw_password=self.validated_data['new_password1']
        )
        user.save()

        return user


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()


class UserViewSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ['profile', 'email', 'id']
