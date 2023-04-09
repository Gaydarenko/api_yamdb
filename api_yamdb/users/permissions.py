from rest_framework import permissions


class IsAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and (request.user.is_superuser or request.user.is_admin))


class Anonimous(permissions.BasePermission):

    def has_permission(self, request, view):
        return True


class OwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if view.action == 'retrieve':
            return request.method in permissions.SAFE_METHODS
        return obj.author == request.user
