from rest_framework import permissions


class IsActiveUser(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        return request.user.is_active is True
