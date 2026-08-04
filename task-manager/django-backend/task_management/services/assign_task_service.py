from django.core.exceptions import PermissionDenied
from django.db import transaction

from notifications.services.create_notification_service import (
    CreateNotificationService,
)
from project_management.selectors.project_selector import ProjectSelector
from task_management.repositories.task_repository import TaskRepository
from task_management.selectors.task_selector import TaskSelector


class AssignTaskService:
    """
    Business logic for assigning a task.
    """

    @staticmethod
    @transaction.atomic
    def execute(
        user,
        task_id,
        assigned_user,
    ):
        """
        Assign or reassign a task.
        """

        task = TaskSelector.get_task_by_id(task_id)

        project = task.project

        # Only project managers or owners can assign tasks
        member = ProjectSelector.get_project_member(
            project=project,
            user=user,
        )

        if (
            project.owner != user
            and (
                member is None
                or member.role != "MANAGER"
            )
        ):
            raise PermissionDenied(
                "You do not have permission to assign tasks."
            )

        # Assigned user must belong to the project
        if not ProjectSelector.is_project_member(
            project,
            assigned_user,
        ):
            raise PermissionDenied(
                "Assigned user is not a member of this project."
            )

        task = TaskRepository.assign_task(
            task,
            assigned_user,
        )

        # Create notification
        CreateNotificationService.notify_task_assigned(task)

        return task