from rest_framework.permissions import BasePermission

from .models import Clan
class HasClan(BasePermission):
    message = "your team should be in a clan to perform this action"
    def has_permission(self, request, view):
        return request.user.team.clan is not None




