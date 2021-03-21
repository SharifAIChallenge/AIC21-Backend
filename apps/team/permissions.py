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


class IsTeamFinalSubmissionCompiled(BasePermission):
    message = "your team's last submission must be compiled"

    def has_permission(self, request, view):
        return request.user.team.submussions.filter(is_final=True) is not None
