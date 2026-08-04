from rest_framework import serializers

from comments.models import Comment


class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer for Comment model.
    """

    user = serializers.StringRelatedField(read_only=True)
    task_title = serializers.CharField(
        source="task.title",
        read_only=True,
    )

    class Meta:
        model = Comment
        fields = (
            "id",
            "task",
            "task_title",
            "user",
            "content",
            "created_at",
            "updated_at",
        )

        read_only_fields = (
            "id",
            "user",
            "task_title",
            "created_at",
            "updated_at",
        )

    def validate_content(self, value):
        """
        Validate comment content.
        """
        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "Comment cannot be empty."
            )

        if len(value) > 1000:
            raise serializers.ValidationError(
                "Comment cannot exceed 1000 characters."
            )

        return value