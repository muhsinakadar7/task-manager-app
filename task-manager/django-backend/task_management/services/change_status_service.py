from django.core.exceptions import PermissionDenied
from django.db import transaction

from notifications.services.create_notification_service import (
    CreateNotificationService,
)
from project_management.selectors.project_selector import ProjectSelector
from task_management.models import Task
from task_management.repositories.task_repository import TaskRepository
from task_management.selectors.task_selector import TaskSelector


class ChangeTaskStatusService:
    """
    Business logic for changing a task's status.
    """

    @staticmethod
    @transaction.atomic
    def execute(
        user,
        task_id,
        status,
    ):
        """
        Change the status of a task.
        """

        task = TaskSelector.get_task_by_id(task_id)

        project = task.project

        # Only project members can change task status
        if not ProjectSelector.is_project_member(
            project,
            user,
        ):
            raise PermissionDenied(
                "You are not a member of this project."
            )

        # Validate status
        valid_statuses = [
            choice[0]
            for choice in Task.Status.choices
        ]

        if status not in valid_statuses:
            raise ValueError(
                "Invalid task status."
            )

        updated_task = TaskRepository.update_task(
            task,
            status=status,
        )

        # Notify when task is completed
        if updated_task.status == Task.Status.COMPLETED:
            CreateNotificationService.notify_task_completed(
                updated_task
            )

        return updated_task