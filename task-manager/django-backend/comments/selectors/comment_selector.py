from django.shortcuts import get_object_or_404

from comments.models import Comment


class CommentSelector:
    """
    Handles all database read operations for Comment.
    """

    @staticmethod
    def get_comment_by_id(comment_id):
        """
        Return a comment by its ID.
        """
        return get_object_or_404(
            Comment.objects.select_related(
                "task",
                "user",
            ),
            id=comment_id,
        )

    @staticmethod
    def get_all_comments():
        """
        Return all comments.
        """
        return Comment.objects.select_related(
            "task",
            "user",
        ).all()

    @staticmethod
    def get_comments_by_task(task):
        """
        Return all comments for a task.
        """
        return Comment.objects.filter(
            task=task,
        ).select_related(
            "task",
            "user",
        )

    @staticmethod
    def get_comments_by_user(user):
        """
        Return all comments created by a user.
        """
        return Comment.objects.filter(
            user=user,
        ).select_related(
            "task",
            "user",
        )