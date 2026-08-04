from django.core.exceptions import PermissionDenied
from django.db import transaction

from notifications.services.create_notification_service import (
    CreateNotificationService,
)
from project_management.selectors.project_selector import ProjectSelector
from task_management.repositories.task_repository import TaskRepository


class CreateTaskService:
    """
    Business logic for creating tasks.
    """

    @staticmethod
    @transaction.atomic
    def execute(user, validated_data):
        """
        Create a new task.
        """

        project = validated_data["project"]

        # Only project members can create tasks
        if not ProjectSelector.is_project_member(
            project,
            user,
        ):
            raise PermissionDenied(
                "You are not a member of this project."
            )

        assigned_to = validated_data.get("assigned_to")

        # Validate assignee
        if assigned_to:
            if not ProjectSelector.is_project_member(
                project,
                assigned_to,
            ):
                raise PermissionDenied(
                    "Assigned user is not a project member."
                )

        task = TaskRepository.create_task(
            **validated_data,
        )

        # Notify assigned user
        if task.assigned_to:
            CreateNotificationService.notify_task_assigned(
                task
            )

        return task