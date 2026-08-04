from django.shortcuts import get_object_or_404

from project_management.models import Project, ProjectMember


class ProjectSelector:
    """
    Handles all database read operations for Project and ProjectMember.
    """

    @staticmethod
    def get_project_by_id(project_id):
        """
        Get a project by its ID.
        """
        return get_object_or_404(Project, id=project_id)

    @staticmethod
    def get_all_projects():
        """
        Return all projects.
        """
        return Project.objects.select_related("owner").all()

    @staticmethod
    def get_projects_by_owner(owner):
        """
        Return all projects owned by a user.
        """
        return Project.objects.filter(
            owner=owner
        ).select_related("owner")

    @staticmethod
    def get_projects_for_user(user):
        """
        Return all projects where the user is a member.
        """
        return Project.objects.filter(
            members__user=user
        ).select_related("owner").distinct()

    @staticmethod
    def get_project_members(project):
        """
        Return all members of a project.
        """
        return ProjectMember.objects.filter(
            project=project
        ).select_related(
            "user",
            "project"
        )

    @staticmethod
    def get_project_member(project, user):
        """
        Return a specific project member.
        """
        return ProjectMember.objects.filter(
            project=project,
            user=user,
        ).first()

    @staticmethod
    def is_project_member(project, user):
        """
        Check whether a user belongs to the project.
        """
        return ProjectMember.objects.filter(
            project=project,
            user=user,
        ).exists()