from rest_framework.permissions import BasePermission
from .models import Invitation


class HasTeam(BasePermission):
    message = "you should be in a team to perform this action"

    def has_permission(self, request, view):
        return request.user.team is not None


class NoTeam(BasePermission):
    message = "you should not be in a team to perform this action"

    def has_permission(self, request, view):
        return request.user.team is None


class TeamHasFinalSubmission(BasePermission):
    message = "your team doesn't have a final submission"

    def has_permission(self, request, view):
        return request.user.team.submissions.filter(is_final=True).first() is not None
