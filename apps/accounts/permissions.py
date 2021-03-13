from rest_framework.permissions import BasePermission


class ProfileComplete(BasePermission):

    def has_permission(self, request, view):
        return request.user.profile.is_complete
