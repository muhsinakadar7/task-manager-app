from rest_framework import status
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from project_management.serializers.project_serializer import ProjectSerializer
from project_management.selectors.project_selector import ProjectSelector
from project_management.services.create_project_service import CreateProjectService
from project_management.services.update_project_service import UpdateProjectService
from project_management.services.delete_project_service import DeleteProjectService


class ProjectListCreateView(ListCreateAPIView):
    """
    List all projects and create a new project.
    """

    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ProjectSelector.get_projects_by_owner(self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        project = CreateProjectService.execute(
            owner=request.user,
            validated_data=serializer.validated_data,
        )

        return Response(
            ProjectSerializer(project).data,
            status=status.HTTP_201_CREATED,
        )


class ProjectDetailView(RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update and delete a project.
    """

    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]
    lookup_url_kwarg = "project_id"

    def get_object(self):
        return ProjectSelector.get_project_by_id(
            self.kwargs["project_id"]
        )

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)

        project = UpdateProjectService.execute(
            project_id=self.kwargs["project_id"],
            user=request.user,
            validated_data=serializer.validated_data,
        )

        return Response(ProjectSerializer(project).data)

    def destroy(self, request, *args, **kwargs):
        DeleteProjectService.execute(
            project_id=self.kwargs["project_id"],
            user=request.user,
        )

        return Response(
            {"message": "Project deleted successfully."},
            status=status.HTTP_204_NO_CONTENT,
        )