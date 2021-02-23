from rest_framework.permissions import BasePermission


class HasTeam(BasePermission):

    def has_permission(self, request, view):
        return request.user.team is not None


class NoTeam(BasePermission):

    def has_permission(self, request, view):
        return request.user.team is None

