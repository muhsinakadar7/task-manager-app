from accounts.repositories.account_repository import AccountRepository
from accounts.selectors.account_selector import AccountSelector


class ProfileService:
    """
    Business logic for user profile.
    """

    @staticmethod
    def get_profile(user_id):
        """
        Return the user profile.
        """
        return AccountSelector.get_user_by_id(user_id)

    @staticmethod
    def update_profile(user, validated_data):
        """
        Update the user's profile.
        """
        return AccountRepository.update_user(user, validated_data)