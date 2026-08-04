from rest_framework.permissions import BasePermission


class IsNotificationRecipient(BasePermission):
    """
    Allows access only to the notification recipient.
    """

    message = "You do not have permission to access this notification."

    def has_object_permission(self, request, view, obj):
        return obj.recipient == request.user


class CanManageNotification(BasePermission):
    """
    Allows the recipient to manage their notifications.
    """

    message = "You do not have permission to manage this notification."

    def has_object_permission(self, request, view, obj):
        return obj.recipient == request.user