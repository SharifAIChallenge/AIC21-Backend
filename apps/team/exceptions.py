from rest_framework.exceptions import APIException
from rest_framework import status


class NoTeamException(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = "You don't have team"
    default_code = "no_team"
