from django.core.exceptions import PermissionDenied
from django.db import transaction

from notifications.repositories.notification_repository import (
    NotificationRepository,
)
from notifications.selectors.notification_selector import (
    NotificationSelector,
)


class DeleteNotificationService:
    """
    Handles business logic for deleting notifications.
    """

    @staticmethod
    @transaction.atomic
    def execute(
        user,
        notification_id,
    ):
        """
        Delete a notification.
        """

        notification = NotificationSelector.get_notification_by_id(
            notification_id
        )

        if notification.recipient != user:
            raise PermissionDenied(
                "You do not have permission to delete this notification."
            )

        NotificationRepository.delete_notification(
            notification
        )

        return True

    @staticmethod
    @transaction.atomic
    def delete_all_read_notifications(
        user,
    ):
        """
        Delete all read notifications for the user.
        """

        notifications = NotificationSelector.get_read_notifications(
            user
        )

        deleted_count = 0

        for notification in notifications:
            NotificationRepository.delete_notification(
                notification
            )
            deleted_count += 1

        return deleted_count