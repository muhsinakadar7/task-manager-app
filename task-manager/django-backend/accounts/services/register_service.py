from accounts.repositories.account_repository import AccountRepository


class RegisterService:
    """
    Business logic for user registration.
    """

    @staticmethod
    def register_user(validated_data):
        """
        Register a new user.
        """

        user = AccountRepository.create_user(validated_data)

        return user