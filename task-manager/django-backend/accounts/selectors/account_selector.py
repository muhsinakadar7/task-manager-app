from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

User = get_user_model()


class AccountSelector:
    """
    Selector class for user database read operations.
    """

    @staticmethod
    def get_user_by_id(user_id):
        """
        Get a user by ID.
        """
        return get_object_or_404(User, id=user_id)

    @staticmethod
    def get_user_by_username(username):
        """
        Get a user by username.
        """
        return User.objects.filter(username=username).first()

    @staticmethod
    def get_user_by_email(email):
        """
        Get a user by email.
        """
        return User.objects.filter(email=email).first()

    @staticmethod
    def get_all_users():
        """
        Return all users.
        """
        return User.objects.all()

    @staticmethod
    def get_active_users():
        """
        Return only active users.
        """
        return User.objects.filter(is_active=True)

    @staticmethod
    def get_staff_users():
        """
        Return all staff users.
        """
        return User.objects.filter(is_staff=True)