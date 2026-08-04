from rest_framework.permissions import BasePermission

from project_management.selectors.project_selector import ProjectSelector
from task_management.selectors.task_selector import TaskSelector


class IsProjectMember(BasePermission):
    """
    Allows access only to project members.
    """

    message = "You are not a member of this project."

    def has_object_permission(self, request, view, obj):
        return ProjectSelector.is_project_member(
            obj.project,
            request.user,
        )


class IsTaskAssignee(BasePermission):
    """
    Allows access only to the assigned user.
    """

    message = "Only the assigned user can perform this action."

    def has_object_permission(self, request, view, obj):
        return obj.assigned_to == request.user


class IsProjectOwner(BasePermission):
    """
    Allows access only to the project owner.
    """

    message = "Only the project owner can perform this action."

    def has_object_permission(self, request, view, obj):
        return obj.project.owner == request.user


class CanManageTask(BasePermission):
    """
    Allows access to the project owner or manager.
    """

    message = "You do not have permission to manage this task."

    def has_object_permission(self, request, view, obj):
        project = obj.project

        if project.owner == request.user:
            return True

        member = ProjectSelector.get_project_member(
            project=project,
            user=request.user,
        )

        if member is None:
            return False

        return member.role == "MANAGER"


class CanViewTask(BasePermission):
    """
    Allows any project member to view a task.
    """

    message = "You are not allowed to view this task."

    def has_object_permission(self, request, view, obj):
        return ProjectSelector.is_project_member(
            obj.project,
            request.user,
        )