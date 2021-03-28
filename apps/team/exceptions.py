from rest_framework.exceptions import APIException
from rest_framework import status


class NoTeamException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "user does not have a team"
    default_code = "no_team"


class TeamIsFullException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "team is full"
    default_code = "team_full"


class HasTeamException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "user has a team"
    default_code = "has_team"


class DuplicatePendingInviteException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "you have a sent an invitation already"
    default_code = "pending_invite"


class NoFinalSubmission(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "target team has no final submission"
    default_code = "no_final_submission"