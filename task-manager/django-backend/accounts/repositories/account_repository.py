from django.contrib.auth import get_user_model

User = get_user_model()


class AccountRepository:
    """
    Repository class for user database write operations.
    """

    @staticmethod
    def create_user(validated_data):
        """
        Create a new user.
        """

        password = validated_data.pop("password")

        validated_data.pop("confirm_password", None)

        user = User(**validated_data)

        user.set_password(password)

        user.save()

        return user

    @staticmethod
    def update_user(user, validated_data):
        """
        Update user details.
        """

        for key, value in validated_data.items():
            setattr(user, key, value)

        user.save()

        return user

    @staticmethod
    def change_password(user, new_password):
        """
        Change the user's password.
        """

        user.set_password(new_password)
        user.save()

        return user

    @staticmethod
    def deactivate_user(user):
        """
        Deactivate a user account.
        """

        user.is_active = False
        user.save()

        return user

    @staticmethod
    def delete_user(user):
        """
        Permanently delete a user.
        """

        user.delete()