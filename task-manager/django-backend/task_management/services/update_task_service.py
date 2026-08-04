from django.core.exceptions import PermissionDenied
from django.db import transaction

from notifications.services.create_notification_service import (
    CreateNotificationService,
)
from project_management.selectors.project_selector import ProjectSelector
from task_management.repositories.task_repository import TaskRepository
from task_management.selectors.task_selector import TaskSelector


class UpdateTaskService:
    """
    Business logic for updating a task.
    """

    @staticmethod
    @transaction.atomic
    def execute(
        user,
        task_id,
        validated_data,
    ):
        """
        Update an existing task.
        """

        task = TaskSelector.get_task_by_id(task_id)

        project = task.project

        # Only project members can update tasks
        if not ProjectSelector.is_project_member(
            project,
            user,
        ):
            raise PermissionDenied(
                "You are not a member of this project."
            )

        old_assigned_to = task.assigned_to

        assigned_to = validated_data.get("assigned_to")

        # If assigned_to is changed,
        # ensure the new user belongs to the project.
        if assigned_to:
            if not ProjectSelector.is_project_member(
                project,
                assigned_to,
            ):
                raise PermissionDenied(
                    "Assigned user is not a project member."
                )

        updated_task = TaskRepository.update_task(
            task,
            **validated_data,
        )

        # Notify if task was reassigned
        if (
            assigned_to is not None
            and assigned_to != old_assigned_to
        ):
            CreateNotificationService.notify_task_assigned(
                updated_task
            )
        else:
            # Notify assigned user about updates
            CreateNotificationService.notify_task_updated(
                updated_task
            )

        return updated_task