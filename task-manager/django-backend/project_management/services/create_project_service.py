from rest_framework.exceptions import ValidationError

from project_management.repositories.project_repository import ProjectRepository
from project_management.selectors.project_selector import ProjectSelector


class CreateProjectService:
    """
    Business logic for creating a project.
    """

    @staticmethod
    def execute(owner, validated_data):
        """
        Create a new project.
        """

        existing_project = (
            ProjectSelector.get_projects_by_owner(owner)
            .filter(name=validated_data["name"])
            .first()
        )

        if existing_project:
            raise ValidationError(
                {
                    "name": "You already have a project with this name."
                }
            )

        project = ProjectRepository.create_project(
            owner=owner,
            validated_data=validated_data,
        )

        ProjectRepository.add_member(
            project=project,
            user=owner,
            role="MANAGER",
        )

        return project