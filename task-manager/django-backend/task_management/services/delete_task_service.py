from django.core.exceptions import PermissionDenied
from django.db import transaction

from project_management.models import ProjectMember
from project_management.selectors.project_selector import ProjectSelector
from task_management.repositories.task_repository import TaskRepository
from task_management.selectors.task_selector import TaskSelector


class DeleteTaskService:
    """
    Business logic for deleting a task.
    """

    @staticmethod
    @transaction.atomic
    def execute(
        user,
        task_id,
    ):
        """
        Delete a task.
        """

        task = TaskSelector.get_task_by_id(task_id)

        project = task.project

        member = ProjectSelector.get_project_member(
            project=project,
            user=user,
        )

        # Only owner or manager can delete tasks
        if (
            project.owner != user
            and (
                member is None
                or member.role != ProjectMember.Role.MANAGER
            )
        ):
            raise PermissionDenied(
                "You do not have permission to delete this task."
            )

        TaskRepository.delete_task(task)

        return True