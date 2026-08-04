from rest_framework.permissions import BasePermission

from project_management.models import ProjectMember
from project_management.selectors.project_selector import ProjectSelector


class IsCommentAuthor(BasePermission):
    """
    Allows access only to the author of the comment.
    """

    message = "Only the comment author can perform this action."

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsProjectMember(BasePermission):
    """
    Allows access only to members of the project's task.
    """

    message = "You are not a member of this project."

    def has_object_permission(self, request, view, obj):
        return ProjectSelector.is_project_member(
            obj.task.project,
            request.user,
        )


class IsProjectOwner(BasePermission):
    """
    Allows access only to the owner of the project.
    """

    message = "Only the project owner can perform this action."

    def has_object_permission(self, request, view, obj):
        return obj.task.project.owner == request.user


class CanManageComment(BasePermission):
    """
    Allows the project owner, project manager,
    or comment author to manage comments.
    """

    message = "You do not have permission to manage this comment."

    def has_object_permission(self, request, view, obj):
        project = obj.task.project

        # Project owner
        if project.owner == request.user:
            return True

        # Comment author
        if obj.user == request.user:
            return True

        # Project manager
        member = ProjectSelector.get_project_member(
            project=project,
            user=request.user,
        )

        if (
            member and
            member.role == ProjectMember.Role.MANAGER
        ):
            return True

        return False


class CanViewComment(BasePermission):
    """
    Allows any project member to view comments.
    """

    message = "You do not have permission to view this comment."

    def has_object_permission(self, request, view, obj):
        return ProjectSelector.is_project_member(
            obj.task.project,
            request.user,
        )