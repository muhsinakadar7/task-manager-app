from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from task_management.serializers.task_report_serializer import (
    TaskReportSerializer,
    TaskSummarySerializer,
)
from task_management.services.report_service import ReportService


class TaskSummaryView(APIView):
    """
    Returns task summary statistics.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        summary = ReportService.get_task_summary()

        serializer = TaskSummarySerializer(summary)

        return Response(serializer.data)


class CompletedTaskListView(ListAPIView):
    """
    Returns completed tasks.
    """

    serializer_class = TaskReportSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ReportService.completed_tasks()


class OverdueTaskListView(ListAPIView):
    """
    Returns overdue tasks.
    """

    serializer_class = TaskReportSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ReportService.overdue_tasks()


class HighPriorityTaskListView(ListAPIView):
    """
    Returns high priority tasks.
    """

    serializer_class = TaskReportSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ReportService.high_priority_tasks()


class TasksByProjectView(APIView):
    """
    Returns task count grouped by project.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = ReportService.tasks_by_project()

        return Response(data)


class TasksByUserView(APIView):
    """
    Returns task count grouped by assigned user.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = ReportService.tasks_by_user()

        return Response(data)