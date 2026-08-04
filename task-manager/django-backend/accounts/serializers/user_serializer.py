from rest_framework import serializers

from accounts.models import User


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for displaying user information.
    """

    class Meta:
        model = User

        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "profile_image",
            "created_at",
            "updated_at",
        )

        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )