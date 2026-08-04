from django.contrib.auth import get_user_model
from rest_framework import serializers

from project_management.models import Project
from task_management.models import Task

User = get_user_model()


class TaskSerializer(serializers.ModelSerializer):
    """
    Serializer for creating, updating and retrieving tasks.
    """

    project = serializers.PrimaryKeyRelatedField(
        queryset=Project.objects.all()
    )

    assigned_to = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        required=False,
        allow_null=True,
    )

    class Meta:
        model = Task
        fields = (
            "id",
            "project",
            "title",
            "description",
            "assigned_to",
            "priority",
            "status",
            "due_date",
            "created_at",
            "updated_at",
        )

        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )

    def validate_title(self, value):
        """
        Ensure title is not empty.
        """
        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "Task title cannot be empty."
            )

        return value

    def validate(self, attrs):
        """
        Cross-field validation.
        """
        project = attrs.get("project")
        assigned_to = attrs.get("assigned_to")

        if project is None:
            raise serializers.ValidationError(
                {"project": "Project is required."}
            )

        if assigned_to and not project.members.filter(
            user=assigned_to
        ).exists():
            raise serializers.ValidationError(
                {
                    "assigned_to": (
                        "Assigned user must be a member "
                        "of the project."
                    )
                }
            )

        return attrs