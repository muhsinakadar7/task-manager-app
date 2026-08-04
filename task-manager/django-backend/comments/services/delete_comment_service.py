from django.core.exceptions import PermissionDenied
from django.db import transaction

from comments.repositories.comment_repository import CommentRepository
from comments.selectors.comment_selector import CommentSelector
from project_management.models import ProjectMember
from project_management.selectors.project_selector import ProjectSelector


class DeleteCommentService:
    """
    Handles business logic for deleting comments.
    """

    @staticmethod
    @transaction.atomic
    def execute(
        user,
        comment_id,
    ):
        """
        Delete a comment.
        """

        comment = CommentSelector.get_comment_by_id(
            comment_id
        )

        project = comment.task.project

        # Project owner can delete any comment
        if project.owner == user:
            CommentRepository.delete_comment(comment)
            return True

        # Comment author can delete their own comment
        if comment.user == user:
            CommentRepository.delete_comment(comment)
            return True

        # Project manager can delete comments
        member = ProjectSelector.get_project_member(
            project,
            user,
        )

        if (
            member
            and member.role == ProjectMember.Role.MANAGER
        ):
            CommentRepository.delete_comment(comment)
            return True

        raise PermissionDenied(
            "You do not have permission to delete this comment."
        )