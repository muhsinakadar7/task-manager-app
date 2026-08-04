from django.core.exceptions import PermissionDenied
from django.db import transaction

from notifications.repositories.notification_repository import (
    NotificationRepository,
)
from notifications.selectors.notification_selector import (
    NotificationSelector,
)


class MarkAsReadService:
    """
    Handles business logic for marking notifications as read.
    """

    @staticmethod
    @transaction.atomic
    def execute(
        user,
        notification_id,
    ):
        """
        Mark a notification as read.
        """

        notification = NotificationSelector.get_notification_by_id(
            notification_id
        )

        if notification.recipient != user:
            raise PermissionDenied(
                "You do not have permission to modify this notification."
            )

        return NotificationRepository.mark_as_read(
            notification
        )

    @staticmethod
    @transaction.atomic
    def mark_all_as_read(user):
        """
        Mark all unread notifications as read.
        """

        notifications = NotificationSelector.get_unread_notifications(
            user
        )

        updated_notifications = []

        for notification in notifications:
            NotificationRepository.mark_as_read(
                notification
            )
            updated_notifications.append(notification)

        return updated_notifications