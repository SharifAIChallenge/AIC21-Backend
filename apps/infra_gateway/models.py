from django.db import models

from model_utils.models import TimeStampedModel


class EventStatusCodeTypes:
    COMPILE_SUCCESS = 100
    COMPILE_FAILED = 102

    # file transfer status codes
    UPLOAD_FAILED = 402
    FILE_NOT_FOUND = 404

    # match status codes
    MATCH_STARTED = 500
    MATCH_FAILED = 502
    MATCH_SUCCESS = 504
    MATCH_TIMEOUT = 506

    Types = (
        (COMPILE_SUCCESS, COMPILE_SUCCESS),
        (COMPILE_FAILED, COMPILE_FAILED),
        (UPLOAD_FAILED, UPLOAD_FAILED),
        (FILE_NOT_FOUND, FILE_NOT_FOUND),
        (MATCH_STARTED, MATCH_STARTED),
        (MATCH_FAILED, MATCH_FAILED),
        (MATCH_SUCCESS, MATCH_SUCCESS),
        (MATCH_TIMEOUT, MATCH_TIMEOUT)
    )


class InfraEventPush(TimeStampedModel):
    title = models.CharField(
        max_length=256
    )
    token = models.CharField(
        max_length=256
    )
    status_code = models.PositiveSmallIntegerField(
        default=200,
        choices=EventStatusCodeTypes.Types
    )
    message_body = models.TextField(
        blank=True,
        null=True
    )
