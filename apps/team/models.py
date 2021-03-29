import os
import logging

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _

from model_utils.models import UUIDModel, TimeStampedModel
from rest_framework.generics import get_object_or_404

from apps.infra_gateway import functions
from .tasks import handle_submission

MAX_MEMBERS = 3

User = get_user_model()

logger = logging.getLogger(__name__)


class Team(UUIDModel, TimeStampedModel):
    IMAGE_MAX_SIZE = 1024 * 1024

    name = models.CharField(max_length=128, unique=True)
    image = models.ImageField(upload_to="teams/images/", null=True,
                              blank=True)  # TODO : Should read path from setting parameters
    creator = models.ForeignKey(to=User,
                                on_delete=models.RESTRICT,
                                related_name='created_teams')
    level_one_payed = models.BooleanField(
        default=False
    )

    def is_complete(self):
        return self.members.count() == MAX_MEMBERS

    def has_final_submission(self):
        return self.submissions.filter(is_final=True).first() is not None

    def reject_all_pending_invitations(self):
        invitations = self.invitations.filter(status="pending")
        invitations.update(status="rejected")

    def member_count(self):
        return self.members.count()

    def wins(self):
        return self.won_matches.count()

    def losses(self):
        from apps.challenge.models import Match

        return Match.objects.filter(
            Q(team1=self) | Q(team2=self)
        ).exclude(winner=self).exclude(winner=None).count()

    def draws(self):
        from apps.challenge.models import Match

        not_draws = self.wins() + self.losses()
        return Match.objects.filter(
            Q(team1=self) | Q(team2=self)
        ).count() - not_draws

    def final_submission(self):
        return self.submissions.filter(
            is_final=True
        ).last()

    def __str__(self):
        return '%s' % self.name


class InvitationTypes:
    TEAM_TO_USER = 'team_to_user'
    USER_TO_TEAM = 'user_to_team'
    TYPES = (
        (TEAM_TO_USER, 'Team to user invitation'),
        (USER_TO_TEAM, 'User to team invitation')
    )


class InvitationStatusTypes:
    PENDING = 'pending'
    ACCEPTED = 'accepted'
    REJECTED = 'rejected'
    TYPES = (
        (PENDING, 'Pending'),
        (ACCEPTED, 'Accepted'),
        (REJECTED, 'Rejected')
    )


class Invitation(UUIDModel, TimeStampedModel):
    user = models.ForeignKey(User, related_name='invitations',
                             on_delete=models.CASCADE)
    team = models.ForeignKey(Team, related_name='invitations',
                             on_delete=models.CASCADE)
    type = models.CharField(max_length=50, choices=InvitationTypes.TYPES)
    status = models.CharField(
        max_length=50,
        choices=InvitationStatusTypes.TYPES,
        default=InvitationStatusTypes.PENDING
    )


class SubmissionLanguagesTypes:
    CPP = 'cpp'
    JAVA = 'java'
    PYTHON3 = 'py3'

    TYPES = (
        (CPP, _('C++')),
        (JAVA, _('Java')),
        (PYTHON3, _('Python 3')),
    )


class SubmissionStatusTypes:
    UPLOADING = 'uploading'
    UPLOADED = 'uploaded'
    COMPILING = 'compiling'
    COMPILED = 'compiled'
    FAILED = 'failed'

    TYPES = (
        (UPLOADING, _('Uploading')),
        (UPLOADED, _('Uploaded')),
        (COMPILING, _('Compiling')),
        (COMPILED, _('Compiled')),
        (FAILED, _('Failed'))
    )


class Submission(models.Model):
    FILE_SIZE_LIMIT = 20 * 1024 * 1024

    team = models.ForeignKey(Team, related_name='submissions',
                             on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='submissions',
                             on_delete=models.CASCADE)
    language = models.CharField(max_length=50,
                                choices=SubmissionLanguagesTypes.TYPES,
                                default=SubmissionLanguagesTypes.JAVA)
    file = models.FileField(null=True, blank=True)
    submit_time = models.DateTimeField(auto_now_add=True)
    is_final = models.BooleanField(default=False)
    status = models.CharField(max_length=50,
                              choices=SubmissionStatusTypes.TYPES,
                              default=SubmissionStatusTypes.UPLOADING)
    infra_compile_message = models.CharField(max_length=1023, null=True,
                                             blank=True)
    infra_token = models.CharField(max_length=256, null=True, blank=True,
                                   unique=True)
    infra_compile_token = models.CharField(max_length=256, null=True,
                                           blank=True, unique=True)
    download_link = models.URLField(max_length=512, null=True, blank=True)

    def __str__(self):
        return "id: " + str(
            self.id) + ' team: ' + self.team.name + " user: " + \
               self.user.username

    def set_final(self):
        """
            Use this method instead of changing the is_final attribute directly
            This makes sure that only one instance of TeamSubmission has
            is_final flag set to True.
        """
        if self.status != 'compiled':
            raise ValueError(_('This submission is not compiled yet.'))
        Submission.objects.filter(is_final=True, team=self.team).update(
            is_final=False)
        self.is_final = True
        self.save()

    def handle(self):
        handle_submission.delay(self.id)
        # handle_submission(self.id)
        pass

    def upload(self):
        from apps.infra_gateway.functions import upload_code

        self.infra_token = upload_code(self)
        self.status = SubmissionStatusTypes.UPLOADED
        self.save()

    def compile(self):
        result = functions.compile_submissions([self])
        if result[0]['success']:
            self.status = SubmissionStatusTypes.COMPILING
            self.infra_compile_token = result[0]['run_id']
        else:
            logger.error(result[0][self.infra_token]['errors'])
        self.save()

    @classmethod
    def update_submission(cls, infra_token, status):
        submission = get_object_or_404(cls, infra_token=infra_token)

        submission.status = status
        submission.save()

        return submission
