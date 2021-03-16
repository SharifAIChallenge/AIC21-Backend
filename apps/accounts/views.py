from django.db.models import F, Value
from django.db.models.functions import Concat
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.utils.http import urlsafe_base64_decode
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.hashers import make_password

from rest_framework import status, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.generics import GenericAPIView

from rest_framework.parsers import FormParser, MultiPartParser, JSONParser

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.accounts.models import MajorAPIConfig
from .permissions import ProfileComplete
from .models import Profile, User, ResetPasswordToken, UniversityAPIConfig, University
from .serializer import (
    UserSerializer, ProfileSerializer, EmailSerializer,
    UserViewSerializer, ChangePasswordSerializer,
    ResetPasswordConfirmSerializer, GoogleLoginSerializer, UniversitySerializer)

__all__ = (
    'LoginAPIView', 'SignUpAPIView', 'ActivateAPIView', 'LogoutAPIView',
    'ResendActivationEmailAPIView', 'ProfileAPIView',
    'ChangePasswordAPIView', 'ResetPasswordAPIView',
    'ResetPasswordConfirmAPIView', 'HideProfileInfoAPIView',
    'UserWithoutTeamAPIView', 'GoogleLoginAPIView', 'IsActivatedAPIView',
    'UniversitySearchAPIView', 'MajorSearchAPIView'
)


class GoogleLoginAPIView(GenericAPIView):
    serializer_class = GoogleLoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.save()

        return Response(
            data={'token': token.key},
            status=status.HTTP_200_OK
        )


LoginAPIView = ObtainAuthToken


class IsActivatedAPIView(GenericAPIView):
    serializer_class = EmailSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        user = get_object_or_404(User, username=data['email'])

        return Response(
            data={'is_active': user.is_active},
            status=status.HTTP_200_OK
        )


class SignUpAPIView(GenericAPIView):
    queryset = Profile.objects.all()
    serializer_class = UserSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        user.send_activation_email()

        return Response(
            data={'detail': _('Check your email for confirmation link')},
            status=200
        )


class ActivateAPIView(GenericAPIView):

    def get(self, request, eid, token):
        User.activate(eid, token)
        return Response(data={'detail': _('Account Activated')},
                        status=status.HTTP_200_OK)


class LogoutAPIView(GenericAPIView):
    queryset = Profile.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


class ResendActivationEmailAPIView(GenericAPIView):
    serializer_class = EmailSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = get_object_or_404(User,
                                     email=serializer.validated_data['email'])
            user.send_activation_email()
            return Response(
                data={'detail': _('Check your email for confirmation link')},
                status=200
            )


class ProfileAPIView(GenericAPIView):
    queryset = User.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def get(self, request):
        user = request.user
        data = self.get_serializer(instance=user.profile).data
        return Response(data={'data': data}, status=status.HTTP_200_OK)

    def put(self, request):
        user = request.user
        serializer = ProfileSerializer(instance=user.profile,
                                       data=request.data,
                                       partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            data={'data': serializer.data},
            status=status.HTTP_200_OK
        )

    def delete(self, request):
        to_be_deleted = self.request.query_params.get('file')
        if not to_be_deleted or to_be_deleted not in ('image', 'resume'):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if to_be_deleted == 'image':
            self.request.user.profile.image = None
        else:
            self.request.user.profile.resume = None

        self.request.user.profile.save()

        return Response(status=status.HTTP_200_OK)


class HideProfileInfoAPIView(GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        request.user.profile.hide_profile_info = (
            not request.user.profile.hide_profile_info
        )

        return Response(
            status=status.HTTP_200_OK
        )


class ChangePasswordAPIView(GenericAPIView):
    queryset = User.objects.all()
    serializer_class = ChangePasswordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            data={'detail': _('password changed successfully')},
            status=200
        )


class ResetPasswordAPIView(GenericAPIView):
    serializer_class = EmailSerializer

    def post(self, request):
        data = self.get_serializer(request.data).data

        user = get_object_or_404(User, email=data['email'])
        user.send_password_confirm_email()

        return Response(
            {'detail': _('Successfully Sent Reset Password Email')},
            status=200)


class ResetPasswordConfirmAPIView(GenericAPIView):
    serializer_class = ResetPasswordConfirmSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        rs_token = get_object_or_404(ResetPasswordToken, uid=data['uid'],
                                     token=data['token'])
        if (
                timezone.now() - rs_token.expiration_date).total_seconds() > 24 * 60 * 60:
            return Response({'error': 'Token Expired'}, status=400)

        user = get_object_or_404(User,
                                 id=urlsafe_base64_decode(data['uid']).decode(
                                     'utf-8'))
        rs_token.delete()
        user.password = make_password(data['new_password1'])
        user.save()
        return Response(data={'detail': _('Successfully Changed Password')},
                        status=200)


class UserWithoutTeamAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated, ProfileComplete]
    serializer_class = UserViewSerializer

    def get(self, request):

        result = self.get_serializer(self.get_queryset(), many=True).data

        return Response({
            "data": result,
        }, status=status.HTTP_200_OK)

    def get_queryset(self):
        name = self.request.query_params.get('name')
        email = self.request.query_params.get('email')
        university = self.request.query_params.get('university')
        programming_language = self.request.query_params.get(
            'programming_language')
        major = self.request.query_params.get('major')

        queryset = User.objects.all().filter(team=None).exclude(profile=None)

        if name:
            queryset = queryset.annotate(
                name=Concat('profile__firstname_fa', Value(' '),
                            'profile__lastname_fa')
            ).filter(name__icontains=name)

        if email:
            queryset = queryset.filter(
                email__icontains=email
            )

        if university:
            queryset = queryset.filter(
                profile__university__icontains=university
            )

        if programming_language:
            queryset = queryset.filter(
                profile__programming_language=programming_language
            )

        if major:
            queryset = queryset.filter(
                profile__major__icontains=major
            )
        complete_profiles = [user.id for user in
                             filter(lambda user: user.profile.is_complete,
                                    queryset
                                    )
                             ]
        queryset = queryset.filter(id__in=complete_profiles)
        return queryset

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['limited'] = True

        return context


class ProfileInfoAPIView(GenericAPIView):
    queryset = User.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = []

    def get(self, request, userid):
        user = get_object_or_404(User, id=userid)
        data = self.get_serializer(user.profile).data
        return Response(data={'data': data}, status=status.HTTP_200_OK)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['limited'] = True
        return context


class UniversitySearchAPIView(GenericAPIView):
    # permission_classes = (IsAuthenticated,)
    serializer_class = UniversitySerializer
    def get(self, request):
        import requests

        api_config = UniversityAPIConfig.objects.last()
        url = api_config.url
        print(url)
        headers = eval(api_config.headers)
        search_param = self.request.query_params.get('q', '')
        payload = f"query={search_param}"
        response = requests.request(
            'POST',
            url,
            headers=headers,
            data=payload.encode('utf-8')
        )
        if(response.status_code == status.HTTP_200_OK):
            for data in response.json()["data"]:
                if not University.objects.all().filter(id=data["id"]).exists():
                    University.objects.create(id=data["id"],name=data["name"],school_type=data["school_type"])
            response = response.json()["data"]
        else:
            universities = University.objects.filter(name__icontains=search_param).order_by('name')[:20]
            response = self.get_serializer(instance=universities,many=True).data
        return Response(
            data={'data': response},
            status=status.HTTP_200_OK
        )


class MajorSearchAPIView(GenericAPIView):
    # permission_classes = (IsAuthenticated,)

    def get(self, request):
        import requests

        api_config = MajorAPIConfig.objects.last()
        url = api_config.url
        headers = eval(api_config.headers)

        url = f'{url}/{self.request.query_params.get("q", "")}'
        print(url)
        response = requests.request(
            'GET',
            url,
            headers=headers,
            data={}
        )

        return Response(
            data={'data': response.json()},
            status=status.HTTP_200_OK
        )
