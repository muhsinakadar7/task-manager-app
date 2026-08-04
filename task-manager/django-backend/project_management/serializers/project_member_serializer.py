from django.contrib.auth import get_user_model
from rest_framework import serializers

from project_management.models import ProjectMember

User = get_user_model()


class ProjectMemberSerializer(serializers.ModelSerializer):
    """
    Serializer for ProjectMember model.
    """

    username = serializers.ReadOnlyField(source="user.username")
    email = serializers.ReadOnlyField(source="user.email")

    class Meta:
        model = ProjectMember

        fields = (
            "id",
            "project",
            "user",
            "username",
            "email",
            "role",
            "joined_at",
        )

        read_only_fields = (
            "id",
            "joined_at",
            "username",
            "email",
        )

    def validate_role(self, value):
        """
        Validate member role.
        """

        valid_roles = [
            "MANAGER",
            "DEVELOPER",
            "TESTER",
        ]

        if value not in valid_roles:
            raise serializers.ValidationError(
                f"Role must be one of: {', '.join(valid_roles)}"
            )

        return value

    def validate_user(self, value):
        """
        Validate selected user.
        """

        if not value.is_active:
            raise serializers.ValidationError(
                "Inactive users cannot be added to a project."
            )

        return value