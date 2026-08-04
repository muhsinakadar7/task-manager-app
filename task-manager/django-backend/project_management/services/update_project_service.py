from rest_framework.exceptions import PermissionDenied

from project_management.repositories.project_repository import ProjectRepository
from project_management.selectors.project_selector import ProjectSelector


class UpdateProjectService:
    """
    Business logic for updating a project.
    """

    @staticmethod
    def execute(project_id, user, validated_data):
        """
        Update a project.
        """

        project = ProjectSelector.get_project_by_id(project_id)

        if project.owner != user:
            raise PermissionDenied(
                "Only the project owner can update this project."
            )

        project = ProjectRepository.update_project(
            project=project,
            validated_data=validated_data,
        )

        return project