from django.core.exceptions import PermissionDenied
from django.db import transaction

from comments.repositories.comment_repository import CommentRepository
from comments.selectors.comment_selector import CommentSelector
from project_management.models import ProjectMember
from project_management.selectors.project_selector import ProjectSelector


class UpdateCommentService:
    """
    Handles business logic for updating comments.
    """

    @staticmethod
    @transaction.atomic
    def execute(
        user,
        comment_id,
        validated_data,
    ):
        """
        Update an existing comment.
        """

        comment = CommentSelector.get_comment_by_id(
            comment_id
        )

        project = comment.task.project

        # Project owner can edit any comment
        if project.owner == user:
            return CommentRepository.update_comment(
                comment,
                **validated_data,
            )

        # Comment author can edit their own comment
        if comment.user == user:
            return CommentRepository.update_comment(
                comment,
                **validated_data,
            )

        # Project manager can also edit comments
        member = ProjectSelector.get_project_member(
            project,
            user,
        )

        if (
            member
            and member.role == ProjectMember.Role.MANAGER
        ):
            return CommentRepository.update_comment(
                comment,
                **validated_data,
            )

        raise PermissionDenied(
            "You do not have permission to update this comment."
        )