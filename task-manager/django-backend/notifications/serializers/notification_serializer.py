from rest_framework import serializers

from notifications.models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    """
    Serializer for Notification model.
    """

    recipient = serializers.StringRelatedField(
        read_only=True,
    )

    notification_type_display = serializers.CharField(
        source="get_notification_type_display",
        read_only=True,
    )

    class Meta:
        model = Notification

        fields = (
            "id",
            "recipient",
            "title",
            "message",
            "notification_type",
            "notification_type_display",
            "is_read",
            "created_at",
        )

        read_only_fields = (
            "id",
            "recipient",
            "created_at",
        )

    def validate_title(self, value):
        """
        Validate notification title.
        """
        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "Title cannot be empty."
            )

        if len(value) > 255:
            raise serializers.ValidationError(
                "Title cannot exceed 255 characters."
            )

        return value

    def validate_message(self, value):
        """
        Validate notification message.
        """
        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "Message cannot be empty."
            )

        return value