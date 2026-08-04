from django.db import transaction

from notifications.models import Notification
from notifications.repositories.notification_repository import (
    NotificationRepository,
)


class CreateNotificationService:
    """
    Handles business logic for creating notifications.
    """

    @staticmethod
    @transaction.atomic
    def execute(
        recipient,
        title,
        message,
        notification_type,
    ):
        """
        Create a notification.

        Args:
            recipient: User who will receive the notification.
            title: Notification title.
            message: Notification message.
            notification_type: Notification.NotificationType value.

        Returns:
            Notification instance.
        """

        notification = NotificationRepository.create_notification(
            recipient=recipient,
            title=title,
            message=message,
            notification_type=notification_type,
        )

        return notification

    @staticmethod
    @transaction.atomic
    def notify_task_assigned(task):
        """
        Notify user that a task has been assigned.
        """

        if task.assigned_to is None:
            return None

        return CreateNotificationService.execute(
            recipient=task.assigned_to,
            title="Task Assigned",
            message=f'You have been assigned the task "{task.title}".',
            notification_type=Notification.NotificationType.TASK_ASSIGNED,
        )

    @staticmethod
    @transaction.atomic
    def notify_task_updated(task):
        """
        Notify assigned user that a task was updated.
        """

        if task.assigned_to is None:
            return None

        return CreateNotificationService.execute(
            recipient=task.assigned_to,
            title="Task Updated",
            message=f'The task "{task.title}" has been updated.',
            notification_type=Notification.NotificationType.TASK_UPDATED,
        )

    @staticmethod
    @transaction.atomic
    def notify_task_completed(task):
        """
        Notify the project owner when a task is completed.
        """

        return CreateNotificationService.execute(
            recipient=task.project.owner,
            title="Task Completed",
            message=f'The task "{task.title}" has been completed.',
            notification_type=Notification.NotificationType.TASK_COMPLETED,
        )

    @staticmethod
    @transaction.atomic
    def notify_comment_added(comment):
        """
        Notify the assigned user when a comment is added.
        """

        task = comment.task

        if task.assigned_to is None:
            return None

        # Avoid notifying users about their own comments
        if task.assigned_to == comment.user:
            return None

        return CreateNotificationService.execute(
            recipient=task.assigned_to,
            title="New Comment",
            message=(
                f'{comment.user.username} commented on '
                f'"{task.title}".'
            ),
            notification_type=Notification.NotificationType.COMMENT_ADDED,
        )

    @staticmethod
    @transaction.atomic
    def notify_project_invitation(
        recipient,
        project,
    ):
        """
        Notify a user that they have been invited to a project.
        """

        return CreateNotificationService.execute(
            recipient=recipient,
            title="Project Invitation",
            message=(
                f'You have been invited to join '
                f'"{project.name}".'
            ),
            notification_type=Notification.NotificationType.PROJECT_INVITATION,
        )