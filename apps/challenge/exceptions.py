from rest_framework.exceptions import APIException
from rest_framework import status


class DuplicatePendingRequestException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "you have a sent an request already"
    default_code = "pending_request"

class SelfRequestException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "you cant send request to your own team"
    default_code = "self_request"