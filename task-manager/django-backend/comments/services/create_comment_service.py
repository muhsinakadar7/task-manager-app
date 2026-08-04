from django.core.exceptions import PermissionDenied
from django.db import transaction

from comments.repositories.comment_repository import CommentRepository
from notifications.services.create_notification_service import (
    CreateNotificationService,
)
from project_management.selectors.project_selector import ProjectSelector


class CreateCommentService:
    """
    Handles business logic for creating comments.
    """

    @staticmethod
    @transaction.atomic
    def execute(user, validated_data):
        """
        Create a new comment.
        """

        task = validated_data["task"]
        project = task.project

        # Only project members can comment
        if not ProjectSelector.is_project_member(
            project,
            user,
        ):
            raise PermissionDenied(
                "You are not a member of this project."
            )

        comment = CommentRepository.create_comment(
            task=task,
            user=user,
            content=validated_data["content"],
        )

        # Notify the assigned user (if applicable)
        CreateNotificationService.notify_comment_added(
            comment
        )

        return comment