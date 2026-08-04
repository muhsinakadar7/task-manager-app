from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.serializers.login_serializer import LoginSerializer
from accounts.serializers.register_serializer import RegisterSerializer
from accounts.serializers.user_serializer import UserSerializer
from accounts.services.login_service import LoginService
from accounts.services.register_service import RegisterService


class RegisterView(APIView):
    """
    API for user registration.
    """

    def post(self, request):

        serializer = RegisterSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        user = RegisterService.register_user(
            serializer.validated_data
        )

        return Response(
            {
                "message": "User registered successfully.",
                "data": UserSerializer(user).data,
            },
            status=status.HTTP_201_CREATED,
        )


class LoginView(APIView):
    """
    API for user login.
    """

    def post(self, request):

        serializer = LoginSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        result = LoginService.login_user(
            serializer.validated_data["user"]
        )

        return Response(
            {
                "message": "Login successful.",
                "access": result["access"],
                "refresh": result["refresh"],
                "user": UserSerializer(result["user"]).data,
            },
            status=status.HTTP_200_OK,
        )