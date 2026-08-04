from rest_framework.permissions import BasePermission

from project_management.selectors.project_selector import ProjectSelector


class IsProjectOwner(BasePermission):
    """
    Allows access only to the project owner.
    """

    message = "Only the project owner can perform this action."

    def has_permission(self, request, view):
        project_id = view.kwargs.get("project_id")

        if not project_id:
            return False

        project = ProjectSelector.get_project_by_id(project_id)

        return project.owner == request.user


class IsProjectMember(BasePermission):
    """
    Allows access only to project members.
    """

    message = "You are not a member of this project."

    def has_permission(self, request, view):
        project_id = view.kwargs.get("project_id")

        if not project_id:
            return False

        project = ProjectSelector.get_project_by_id(project_id)

        return ProjectSelector.is_project_member(
            project=project,
            user=request.user,
        )


class IsProjectManager(BasePermission):
    """
    Allows access only to project managers.
    """

    message = "Only project managers can perform this action."

    def has_permission(self, request, view):
        project_id = view.kwargs.get("project_id")

        if not project_id:
            return False

        project = ProjectSelector.get_project_by_id(project_id)

        member = ProjectSelector.get_project_member(
            project=project,
            user=request.user,
        )

        if member is None:
            return False

        return member.role == "MANAGER"