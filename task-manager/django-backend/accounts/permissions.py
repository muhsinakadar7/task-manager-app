from rest_framework.permissions import BasePermission


class IsStaffUser(BasePermission):
    """
    Allows access only to staff users.
    """

    message = "Only staff users are allowed."

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.is_staff
        )


class IsSuperUser(BasePermission):
    """
    Allows access only to superusers.
    """

    message = "Only superusers are allowed."

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.is_superuser
        )


class IsOwner(BasePermission):
    """
    Allows users to access only their own object.
    """

    message = "You do not have permission to access this resource."

    def has_object_permission(self, request, view, obj):
        return obj.id == request.user.id


class IsActiveUser(BasePermission):
    """
    Allows access only to active users.
    """

    message = "Your account is inactive."

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.is_active
        )