from rest_framework import status
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from comments.models import Comment
from comments.selectors.comment_selector import CommentSelector
from comments.serializers.comment_serializer import CommentSerializer
from comments.services.create_comment_service import (
    CreateCommentService,
)
from comments.services.update_comment_service import (
    UpdateCommentService,
)
from comments.services.delete_comment_service import (
    DeleteCommentService,
)
from task_management.selectors.task_selector import TaskSelector


class CommentListCreateView(ListCreateAPIView):
    """
    List all comments or create a new comment.
    """

    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        task_id = self.request.query_params.get("task")

        if task_id:
            task = TaskSelector.get_task_by_id(task_id)
            return CommentSelector.get_comments_by_task(task)

        return CommentSelector.get_all_comments()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        comment = CreateCommentService.execute(
            request.user,
            serializer.validated_data,
        )

        return Response(
            CommentSerializer(comment).data,
            status=status.HTTP_201_CREATED,
        )


class CommentDetailView(RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update and delete a comment.
    """

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def partial_update(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)

        comment = UpdateCommentService.execute(
            request.user,
            kwargs["pk"],
            serializer.validated_data,
        )

        return Response(
            CommentSerializer(comment).data
        )

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data,
            partial=False,
        )
        serializer.is_valid(raise_exception=True)

        comment = UpdateCommentService.execute(
            request.user,
            kwargs["pk"],
            serializer.validated_data,
        )

        return Response(
            CommentSerializer(comment).data
        )

    def destroy(self, request, *args, **kwargs):
        DeleteCommentService.execute(
            request.user,
            kwargs["pk"],
        )

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )