from comments.models import Comment


class CommentRepository:
    """
    Handles all database write operations for Comment.
    """

    @staticmethod
    def create_comment(**validated_data):
        """
        Create a new comment.
        """
        return Comment.objects.create(**validated_data)

    @staticmethod
    def update_comment(comment, **validated_data):
        """
        Update an existing comment.
        """
        for field, value in validated_data.items():
            setattr(comment, field, value)

        comment.save()

        return comment

    @staticmethod
    def delete_comment(comment):
        """
        Delete a comment.
        """
        comment.delete()