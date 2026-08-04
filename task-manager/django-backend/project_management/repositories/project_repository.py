from project_management.models import Project, ProjectMember


class ProjectRepository:
    """
    Handles database write operations for Project and ProjectMember.
    """

    @staticmethod
    def create_project(owner, validated_data):
        """
        Create a new project.
        """

        return Project.objects.create(
            owner=owner,
            **validated_data
        )

    @staticmethod
    def update_project(project, validated_data):
        """
        Update project details.
        """

        for field, value in validated_data.items():
            setattr(project, field, value)

        project.save()

        return project

    @staticmethod
    def delete_project(project):
        """
        Delete a project.
        """

        project.delete()

    @staticmethod
    def add_member(project, user, role):
        """
        Add a user to the project.
        """

        return ProjectMember.objects.create(
            project=project,
            user=user,
            role=role,
        )

    @staticmethod
    def remove_member(project, user):
        """
        Remove a user from a project.
        """

        ProjectMember.objects.filter(
            project=project,
            user=user,
        ).delete()