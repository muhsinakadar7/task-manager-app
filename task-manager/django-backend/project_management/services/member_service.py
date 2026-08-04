from django.core.exceptions import PermissionDenied
from django.db import transaction

from notifications.services.create_notification_service import (
    CreateNotificationService,
)
from project_management.models import ProjectMember
from project_management.repositories.project_repository import (
    ProjectRepository,
)
from project_management.selectors.project_selector import (
    ProjectSelector,
)


class MemberService:
    """
    Business logic for managing project members.
    """

    @staticmethod
    @transaction.atomic
    def add_member(
        owner,
        project_id,
        user,
        role="DEVELOPER",
    ):
        """
        Add a member to a project.
        """

        project = ProjectSelector.get_project_by_id(
            project_id
        )

        # Only project owner can add members
        if project.owner != owner:
            raise PermissionDenied(
                "Only the project owner can add members."
            )

        # User is already a member
        if ProjectSelector.is_project_member(
            project,
            user,
        ):
            raise PermissionDenied(
                "User is already a project member."
            )

        member = ProjectRepository.add_member(
            project=project,
            user=user,
            role=role,
        )

        # Send notification
        CreateNotificationService.notify_project_invitation(
            recipient=user,
            project=project,
        )

        return member

    @staticmethod
    @transaction.atomic
    def remove_member(
        owner,
        project_id,
        user,
    ):
        """
        Remove a member from a project.
        """

        project = ProjectSelector.get_project_by_id(
            project_id
        )

        if project.owner != owner:
            raise PermissionDenied(
                "Only the project owner can remove members."
            )

        member = ProjectSelector.get_project_member(
            project,
            user,
        )

        if member is None:
            raise PermissionDenied(
                "User is not a project member."
            )

        member.delete()

        return True