from notifications.models import Notification


class NotificationRepository:
    """
    Handles all database write operations for Notification.
    """

    @staticmethod
    def create_notification(**validated_data):
        """
        Create a new notification.
        """
        return Notification.objects.create(
            **validated_data,
        )

    @staticmethod
    def update_notification(
        notification,
        **validated_data,
    ):
        """
        Update an existing notification.
        """
        for field, value in validated_data.items():
            setattr(
                notification,
                field,
                value,
            )

        notification.save()

        return notification

    @staticmethod
    def mark_as_read(notification):
        """
        Mark a notification as read.
        """
        notification.is_read = True
        notification.save(
            update_fields=[
                "is_read",
            ],
        )

        return notification

    @staticmethod
    def mark_as_unread(notification):
        """
        Mark a notification as unread.
        """
        notification.is_read = False
        notification.save(
            update_fields=[
                "is_read",
            ],
        )

        return notification

    @staticmethod
    def delete_notification(notification):
        """
        Delete a notification.
        """
        notification.delete()