from rest_framework import serializers

from project_management.models import Project


class ProjectSerializer(serializers.ModelSerializer):
    """
    Serializer for Project model.
    """

    owner = serializers.ReadOnlyField(source="owner.username")

    class Meta:
        model = Project

        fields = (
            "id",
            "name",
            "description",
            "owner",
            "status",
            "start_date",
            "end_date",
            "created_at",
            "updated_at",
        )

        read_only_fields = (
            "id",
            "owner",
            "created_at",
            "updated_at",
        )

    def validate_name(self, value):
        """
        Validate project name.
        """

        value = value.strip()

        if len(value) < 3:
            raise serializers.ValidationError(
                "Project name must contain at least 3 characters."
            )

        return value

    def validate(self, attrs):
        """
        Validate project dates.
        """

        start_date = attrs.get("start_date")
        end_date = attrs.get("end_date")

        if start_date and end_date:
            if end_date < start_date:
                raise serializers.ValidationError(
                    {
                        "end_date": "End date cannot be earlier than start date."
                    }
                )

        return attrs