from django.db import models
import os
from model_utils.models import UUIDModel, TimeStampedModel

MAX_MEMBERS = 3

class Team(UUIDModel,TimeStampedModel):
    name = models.CharField(max_length=128, unique=True)
    image = models.ImageField(upload_to="teams/images/", null=True, blank=True) # TODO : Should read path from setting parameters
    creator = models.ForeignKey(to='accounts.User', on_delete=models.CASCADE, related_name='created_teams')

    def is_complete(self):
        return self.members.count() == MAX_MEMBERS

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

class Invitation(UUIDModel,TimeStampedModel):
    source = models.ForeignKey('accounts.User', related_name='invites', on_delete=models.CASCADE)
    target = models.ForeignKey('accounts.User', related_name='invitations', on_delete=models.CASCADE)
    type = models.CharField(max_length=50, choices=InvitationTypes.TYPES)
    status = models.CharField(
        max_length=50, 
        choices=InvitationStatusTypes.TYPES,
        default=InvitationStatusTypes.PENDING
    )

