from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.serializers.profile_serializer import ProfileSerializer
from accounts.services.profile_service import ProfileService


class ProfileView(APIView):
    """
    Retrieve and update the logged-in user's profile.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Get logged-in user profile.
        """

        user = ProfileService.get_profile(request.user.id)

        serializer = ProfileSerializer(user)

        return Response(
            {
                "message": "Profile fetched successfully.",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    def put(self, request):
        """
        Update logged-in user profile.
        """

        serializer = ProfileSerializer(
            request.user,
            data=request.data,
            partial=True
        )

        serializer.is_valid(raise_exception=True)

        user = ProfileService.update_profile(
            request.user,
            serializer.validated_data
        )

        return Response(
            {
                "message": "Profile updated successfully.",
                "data": ProfileSerializer(user).data,
            },
            status=status.HTTP_200_OK,
        )