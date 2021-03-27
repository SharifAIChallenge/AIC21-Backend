from django.db import models
from apps.accounts.models import User

from model_utils.models import UUIDModel, TimeStampedModel


class TicketStatus:
    OPEN = 'open'
    CLOSED = 'closed'

    TYPES = (
        (OPEN, OPEN),
        (CLOSED, CLOSED),
    )


class ReplyStatus:
    PENDING = 'pending'
    ANSWERED = 'answered'

    TYPES = (
        (PENDING, PENDING),
        (ANSWERED, ANSWERED),
    )


class Ticket(UUIDModel, TimeStampedModel):
    author = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='tickets'
    )

    tag = models.ForeignKey(
        to='ticket.Tag',
        related_name='tickets',
        on_delete=models.DO_NOTHING
    )

    title = models.CharField(
        max_length=50
    )
    text = models.TextField(
        max_length=10000
    )

    is_public = models.BooleanField(
        default=False
    )

    status = models.CharField(
        max_length=32,
        default=TicketStatus.OPEN,
        choices=TicketStatus.TYPES
    )

    def __str__(self):
        return f'{self.title} {self.author.username}'


class Reply(UUIDModel, TimeStampedModel):
    ticket = models.ForeignKey(
        to=Ticket,
        on_delete=models.CASCADE,
        related_name='replies'
    )
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='ticket_replies'
    )
    text = models.TextField()

    status = models.CharField(
        max_length=32,
        default=ReplyStatus.PENDING,
        choices=ReplyStatus.TYPES
    )

    def __str__(self):
        return f'{self.user}'


class Tag(UUIDModel, TimeStampedModel):
    title = models.CharField(
        max_length=128,
    )

    def __str__(self):
        return f'{self.title}'
