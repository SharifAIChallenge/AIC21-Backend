from django.conf import settings

from rest_framework.permissions import BasePermission


class IsInfra(BasePermission):
    message = "you should be in a team to perform this action"

    def has_permission(self, request, view):
        return request.headers['Authorization'] == settings.INFRA_TOKEN
