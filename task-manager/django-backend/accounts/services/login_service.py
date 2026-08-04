from rest_framework_simplejwt.tokens import RefreshToken


class LoginService:
    """
    Business logic for user login.
    """

    @staticmethod
    def login_user(user):
        """
        Generate JWT tokens for the authenticated user.
        """

        refresh = RefreshToken.for_user(user)

        return {
            "user": user,
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }