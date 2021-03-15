from rest_framework.permissions import BasePermission
#todo: move token to config
INFRA_TOKEN = "random_token"

class IsInfra(BasePermission):

    message = "you should be in a team to perform this action"

    def has_permission(self, request, view):
        return request.data['token'] == INFRA_TOKEN

