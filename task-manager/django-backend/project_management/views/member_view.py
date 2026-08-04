from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from project_management.selectors.project_selector import ProjectSelector
from project_management.serializers.project_member_serializer import (
    ProjectMemberSerializer,
)
from project_management.services.member_service import MemberService


class ProjectMemberListView(ListAPIView):
    """
    List all members of a project.
    """

    serializer_class = ProjectMemberSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        project = ProjectSelector.get_project_by_id(
            self.kwargs["project_id"]
        )

        return ProjectSelector.get_project_members(project)


class AddProjectMemberView(APIView):
    """
    Add a user to a project.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request, project_id):

        serializer = ProjectMemberSerializer(
            data=request.data
        )

        serializer.is_valid(raise_exception=True)

        member = MemberService.add_member(
            project_id=project_id,
            owner=request.user,
            user_id=serializer.validated_data["user"].id,
            role=serializer.validated_data["role"],
        )

        return Response(
            ProjectMemberSerializer(member).data,
            status=status.HTTP_201_CREATED,
        )


class RemoveProjectMemberView(APIView):
    """
    Remove a user from a project.
    """

    permission_classes = [IsAuthenticated]

    def delete(self, request, project_id, user_id):

        MemberService.remove_member(
            project_id=project_id,
            owner=request.user,
            user_id=user_id,
        )

        return Response(
            {
                "message": "Member removed successfully."
            },
            status=status.HTTP_204_NO_CONTENT,
        )