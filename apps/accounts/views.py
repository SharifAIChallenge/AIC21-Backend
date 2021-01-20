from django.shortcuts import render, get_object_or_404
from django.utils.translation import gettext_lazy as _
from rest_framework import status, permissions

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.generics import GenericAPIView

from .models import Profile, User
from .serializer import (
    UserSerializer, ProfileSerializer, EmailSerializer,
    UserViewSerializer
)
from rest_framework.response import Response

__all__ = ('LoginAPIView', 'SignUpAPIView', 'ActivateAPIView', 'LogoutAPIView',
           'ResendActivationEmailAPIView', 'ProfileAPIView')

LoginAPIView = ObtainAuthToken


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
    serializer_class = ProfileSerializer
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
    serializer_class = UserViewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        data = self.get_serializer(user).data
        return Response(data={'user': data}, status=status.HTTP_200_OK)

    def put(self, request):
        user = request.user
        serializer = self.get_serializer(instance=user, data=request.data,
                                         partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(self.get_serializer(user).data,
                        status=status.HTTP_200_OK)
