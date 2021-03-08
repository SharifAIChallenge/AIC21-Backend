from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model


class EmailAuthenticationBackend(BaseBackend):
    """
    Custom Email Backend to perform authentication via email
    """

    def authenticate(self, username=None, password=None):
        user_model = get_user_model()
        try:
            user = user_model.objects.get(email=username, is_active=True)
            if user.check_password(password):
                return user
        except user_model.DoesNotExist:
            return None

    def get_user(self, user_id):
        user_model = get_user_model()
        try:
            return user_model.objects.get(pk=user_id)
        except user_model.DoesNotExist:
            return None


class PhoneNumberAuthenticationBackend(BaseBackend):
    """
    Custom Email Backend to perform authentication via phone number
    """

    def authenticate(self, username=None, password=None):
        user_model = get_user_model()
        try:
            user = user_model.objects.get(phone_number=username, is_active=True)
            if user.check_password(password):
                return user
        except user_model.DoesNotExist:
            return None

    def get_user(self, user_id):
        user_model = get_user_model()
        try:
            return user_model.objects.get(pk=user_id)
        except user_model.DoesNotExist:
            return None
