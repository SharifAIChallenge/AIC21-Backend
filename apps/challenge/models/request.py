from django.db import models
from model_utils.models import TimeStampedModel


class RequestStatusTypes:
    PENDING = 'pending'
    REJECTED = 'rejected'
    ACCEPTED = 'accepted'
    TYPES = (
        (PENDING, 'Pending'),
        (REJECTED, 'Rejected'),
        (ACCEPTED, 'Accepted')
    )


class RequestTypes:
    FRIENDLY_MATCH = 'friendly_match'
    CLAN_INVITE = 'clan_invite'
    CLANWAR = 'clanwar'
    TYPES = (
        (FRIENDLY_MATCH, 'Friendly match'),
        (CLAN_INVITE, 'Clan invite'),
        (CLANWAR, 'Clanwar')
    )


class Request(TimeStampedModel):
    source_team = models.ForeignKey(to='team.Team', on_delete=models.CASCADE, related_name='sent_requests')
    target_team = models.ForeignKey(to='team.Team', on_delete=models.CASCADE, related_name='received_request')
    status = models.CharField(
        max_length=50,
        choices=RequestStatusTypes.TYPES,
        default=RequestStatusTypes.PENDING
    )
    type = models.CharField(
        max_length=50,
        choices=RequestTypes.TYPES
    )
