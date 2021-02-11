import secrets

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.encoding import force_bytes
from django.utils.translation import gettext_lazy as _
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from django.db import models
from django.contrib.auth.models import AbstractUser

from apps.core.utils import send_email


class User(AbstractUser):

    def send_activation_email(self):
        activate_user_token = ActivateUserToken(
            token=secrets.token_urlsafe(32),
            eid=urlsafe_base64_encode(force_bytes(self.email)),
        )
        activate_user_token.save()

        context = {
            'domain': settings.DOMAIN,
            'eid': activate_user_token.eid,
            'token': activate_user_token.token,
            'first_name': self.profile.firstname_en
        }

        send_email(
            subject='فعالسازی اکانت AIC21',
            context=context,
            template_name='accounts/email/user_activate_email.html',
            receipts=[self.email]
        )

    def send_password_confirm_email(self):
        uid = urlsafe_base64_encode(force_bytes(self.id))
        ResetPasswordToken.objects.filter(uid=uid).delete()
        reset_password_token = ResetPasswordToken(
            uid=uid,
            token=secrets.token_urlsafe(32),
            expiration_date=timezone.now() + timezone.timedelta(hours=24),
        )
        reset_password_token.save()
        context = {
            'domain': 'aichallenge.sharif.edu',
            'username': self.username,
            'uid': reset_password_token.uid,
            'token': reset_password_token.token,
        }
        send_email(
            subject='تغییر رمز عبور AIC21',
            context=context,
            template_name='accounts/email/user_reset_password.html',
            receipts=[self.email]
        )

    @classmethod
    def activate(cls, eid, token):
        activate_user_token = get_object_or_404(ActivateUserToken,
                                                eid=eid, token=token)

        email = urlsafe_base64_decode(eid).decode('utf-8')
        user = cls.objects.get(email=email)
        user.is_active = True
        activate_user_token.delete()
        user.save()


class Profile(models.Model):
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                related_name='profile'
                                )
    firstname_fa = models.TextField(max_length=30)
    firstname_en = models.TextField(max_length=30)
    lastname_fa = models.TextField(max_length=30)
    lastname_en = models.TextField(max_length=30)
    university = models.CharField(max_length=50)
    province = models.CharField(max_length=128)
    major = models.CharField(max_length=50)
    birth_date = models.CharField(
        max_length=128,
        blank=True,
        null=True
    )

    def __str__(self):
        return f'username: {self.user.username},' \
               f'name: {self.firstname_en} {self.lastname_en},' \
               f'email: {self.user.email}'


class ActivateUserToken(models.Model):
    token = models.CharField(max_length=100)
    eid = models.CharField(max_length=100, null=True)


class ResetPasswordToken(models.Model):
    uid = models.CharField(max_length=100)
    token = models.CharField(max_length=100)
    expiration_date = models.DateTimeField()
