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
import os


class DegreeTypes:
    ST = 'دانش‌ آموز'
    BA = 'کارشناسی'
    MA = 'کارشناسی ارشد'
    DO = 'دکترا'

    TYPES = (
        ('ST', ST),
        ('BA', BA),
        ('MA', MA),
        ('DO', DO)
    )


class User(AbstractUser):
    team = models.ForeignKey(to='team.Team',
                             on_delete=models.SET_NULL,
                             related_name='members', null=True, blank=True)

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

    def reject_all_pending_invites(self):
        invitations = self.invitations.filter(status="pending")
        invitations.update(status="rejected")

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
    IMAGE_MAX_SIZE = 1024 * 1024

    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                related_name='profile'
                                )

    # Personal Info
    firstname_fa = models.CharField(max_length=64, blank=True, null=True)
    firstname_en = models.CharField(max_length=64, blank=True, null=True)
    lastname_fa = models.CharField(max_length=64, blank=True, null=True)
    lastname_en = models.CharField(max_length=64, blank=True, null=True)
    birth_date = models.CharField(max_length=128, blank=True, null=True)
    province = models.CharField(max_length=64, blank=True, null=True)
    phone_number = models.CharField(max_length=32, blank=True, null=True)
    programming_language = models.CharField(max_length=32, blank=True,
                                            null=True)

    # Academic Info
    university = models.CharField(max_length=128, blank=True, null=True)
    major = models.CharField(max_length=64, blank=True, null=True)
    university_term = models.PositiveSmallIntegerField(null=True)
    university_degree = models.CharField(choices=DegreeTypes.TYPES,
                                         max_length=32, null=True)

    # Job Info
    linkedin = models.CharField(max_length=512, blank=True, null=True)
    github = models.CharField(max_length=512, null=True, blank=True)

    # Others
    image = models.ImageField(null=True, blank=True)
    hide_profile_info = models.BooleanField(default=False)

    resume = models.FileField(upload_to="resume", null=True, blank=True)

    @property
    def is_complete(self):
        return all(
            (
                self.university, self.university_degree, self.major,
                self.phone_number, self.birth_date
            )
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


class Skill(models.Model):
    skill = models.CharField(max_length=512)
    profile = models.ForeignKey(to=Profile,
                                related_name='skills',
                                on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.skill}'


class JobExperience(models.Model):
    company = models.CharField(max_length=128)
    position = models.CharField(max_length=256)
    description = models.CharField(max_length=1024, blank=True, null=True)
    profile = models.ForeignKey(
        to=Profile,
        related_name='jobs',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f'{self.position}'
