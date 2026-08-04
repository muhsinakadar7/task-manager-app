from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class ProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for viewing and updating the logged-in user's profile.
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
            "username",
            "created_at",
            "updated_at",
        )