from rest_framework.exceptions import PermissionDenied

from project_management.repositories.project_repository import ProjectRepository
from project_management.selectors.project_selector import ProjectSelector


class DeleteProjectService:
    """
    Business logic for deleting a project.
    """

    @staticmethod
    def execute(project_id, user):
        """
        Delete a project.
        """

        project = ProjectSelector.get_project_by_id(project_id)

        if project.owner != user:
            raise PermissionDenied(
                "Only the project owner can delete this project."
            )

        ProjectRepository.delete_project(project)

        return True