from django.shortcuts import get_object_or_404

from notifications.models import Notification


class NotificationSelector:
    """
    Handles all database read operations for Notification.
    """

    @staticmethod
    def get_notification_by_id(notification_id):
        """
        Return a notification by its ID.
        """
        return get_object_or_404(
            Notification.objects.select_related(
                "recipient",
            ),
            id=notification_id,
        )

    @staticmethod
    def get_notifications_by_user(user):
        """
        Return all notifications for a user.
        """
        return (
            Notification.objects.filter(
                recipient=user,
            )
            .select_related("recipient")
            .order_by("-created_at")
        )

    @staticmethod
    def get_unread_notifications(user):
        """
        Return unread notifications for a user.
        """
        return (
            Notification.objects.filter(
                recipient=user,
                is_read=False,
            )
            .select_related("recipient")
            .order_by("-created_at")
        )

    @staticmethod
    def get_read_notifications(user):
        """
        Return read notifications for a user.
        """
        return (
            Notification.objects.filter(
                recipient=user,
                is_read=True,
            )
            .select_related("recipient")
            .order_by("-created_at")
        )

    @staticmethod
    def count_unread_notifications(user):
        """
        Return unread notification count.
        """
        return Notification.objects.filter(
            recipient=user,
            is_read=False,
        ).count()

    @staticmethod
    def get_recent_notifications(
        user,
        limit=10,
    ):
        """
        Return the most recent notifications.
        """
        return (
            Notification.objects.filter(
                recipient=user,
            )
            .select_related("recipient")
            .order_by("-created_at")[:limit]
        )