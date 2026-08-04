from rest_framework import serializers

from task_management.models import Task


class TaskReportSerializer(serializers.ModelSerializer):
    """
    Serializer used for task reports.
    """

    project = serializers.CharField(
        source="project.name",
        read_only=True,
    )

    assigned_to = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = (
            "id",
            "title",
            "project",
            "assigned_to",
            "priority",
            "status",
            "due_date",
            "created_at",
        )

    def get_assigned_to(self, obj):
        """
        Return assigned user's username.
        """
        if obj.assigned_to:
            return obj.assigned_to.username
        return None


class TaskSummarySerializer(serializers.Serializer):
    """
    Serializer for dashboard summary.
    """

    total_tasks = serializers.IntegerField()
    completed_tasks = serializers.IntegerField()
    pending_tasks = serializers.IntegerField()
    in_progress_tasks = serializers.IntegerField()
    overdue_tasks = serializers.IntegerField()