from django.db.models import QuerySet
from django.utils import timezone
from django.shortcuts import get_object_or_404

from task_management.models import Task


class TaskSelector:
    """
    Selector responsible for database read operations
    related to Task.
    """

    @staticmethod
    def get_task_by_id(task_id: int) -> Task:
        """
        Return a single task.
        """
        return get_object_or_404(
            Task.objects.select_related(
                "project",
                "assigned_to",
            ),
            id=task_id,
        )

    @staticmethod
    def get_all_tasks() -> QuerySet:
        """
        Return all tasks.
        """
        return Task.objects.select_related(
            "project",
            "assigned_to",
        ).all()

    @staticmethod
    def get_tasks_by_project(project):
        """
        Return tasks belonging to a project.
        """
        return Task.objects.select_related(
            "assigned_to",
        ).filter(
            project=project,
        )

    @staticmethod
    def get_tasks_by_user(user):
        """
        Return tasks assigned to a user.
        """
        return Task.objects.select_related(
            "project",
        ).filter(
            assigned_to=user,
        )

    @staticmethod
    def get_tasks_by_status(status):
        """
        Return tasks by status.
        """
        return Task.objects.select_related(
            "project",
            "assigned_to",
        ).filter(
            status=status,
        )

    @staticmethod
    def get_tasks_by_priority(priority):
        """
        Return tasks by priority.
        """
        return Task.objects.select_related(
            "project",
            "assigned_to",
        ).filter(
            priority=priority,
        )

    @staticmethod
    def get_completed_tasks():
        """
        Return completed tasks.
        """
        return Task.objects.filter(
            status=Task.Status.COMPLETED,
        )

    @staticmethod
    def get_pending_tasks():
        """
        Return pending tasks.
        """
        return Task.objects.exclude(
            status=Task.Status.COMPLETED,
        )

    @staticmethod
    def get_overdue_tasks():
        """
        Return overdue tasks.
        """
        today = timezone.now().date()

        return Task.objects.filter(
            due_date__lt=today,
        ).exclude(
            status=Task.Status.COMPLETED,
        )