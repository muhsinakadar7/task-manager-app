from django.conf import settings
from django.db import models


class Notification(models.Model):
    """
    Notification model for user alerts.
    """

    class NotificationType(models.TextChoices):
        TASK_ASSIGNED = "TASK_ASSIGNED", "Task Assigned"
        TASK_UPDATED = "TASK_UPDATED", "Task Updated"
        TASK_COMPLETED = "TASK_COMPLETED", "Task Completed"
        COMMENT_ADDED = "COMMENT_ADDED", "Comment Added"
        PROJECT_INVITATION = "PROJECT_INVITATION", "Project Invitation"

    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications",
    )

    title = models.CharField(
        max_length=255,
    )

    message = models.TextField()

    notification_type = models.CharField(
        max_length=30,
        choices=NotificationType.choices,
    )

    is_read = models.BooleanField(
        default=False,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"

    def __str__(self):
        return f"{self.recipient.username} - {self.title}"