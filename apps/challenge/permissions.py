from rest_framework.permissions import BasePermission

from apps.challenge.models import ClanTeam
from .models import Clan


class HasClan(BasePermission):
    message = "your team should be in a clan to perform this action"

    def has_permission(self, request, view):
        return ClanTeam.objects.filter(team=request.user.team).exists()


class NoClan(BasePermission):
    message = "your team should not be a part of any clan to do this action"

    def has_permission(self, request, view):
        return not ClanTeam.objects.filter(team=request.user.team).exists()
