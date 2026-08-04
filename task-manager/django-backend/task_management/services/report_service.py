from django.db.models import Count
from django.utils import timezone

from task_management.models import Task


class ReportService:
    """
    Service responsible for generating task reports.
    """

    @staticmethod
    def get_task_summary():
        """
        Return dashboard summary.
        """

        today = timezone.now().date()

        return {
            "total_tasks": Task.objects.count(),
            "completed_tasks": Task.objects.filter(
                status=Task.Status.COMPLETED
            ).count(),
            "pending_tasks": Task.objects.filter(
                status=Task.Status.TODO
            ).count(),
            "in_progress_tasks": Task.objects.filter(
                status=Task.Status.IN_PROGRESS
            ).count(),
            "overdue_tasks": Task.objects.filter(
                due_date__lt=today
            ).exclude(
                status=Task.Status.COMPLETED
            ).count(),
        }

    @staticmethod
    def tasks_by_project():
        """
        Return task count grouped by project.
        """

        return (
            Task.objects.values("project__id", "project__name")
            .annotate(total_tasks=Count("id"))
            .order_by("project__name")
        )

    @staticmethod
    def tasks_by_user():
        """
        Return task count grouped by assigned user.
        """

        return (
            Task.objects.values(
                "assigned_to__id",
                "assigned_to__username",
            )
            .annotate(total_tasks=Count("id"))
            .order_by("assigned_to__username")
        )

    @staticmethod
    def completed_tasks():
        """
        Return completed tasks.
        """

        return Task.objects.filter(
            status=Task.Status.COMPLETED
        )

    @staticmethod
    def overdue_tasks():
        """
        Return overdue tasks.
        """

        today = timezone.now().date()

        return Task.objects.filter(
            due_date__lt=today
        ).exclude(
            status=Task.Status.COMPLETED
        )

    @staticmethod
    def high_priority_tasks():
        """
        Return high-priority tasks.
        """

        return Task.objects.filter(
            priority=Task.Priority.HIGH
        )