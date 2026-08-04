from django.urls import path

from comments.views.comment_view import (
    CommentDetailView,
    CommentListCreateView,
)

app_name = "comments"

urlpatterns = [
    path(
        "",
        CommentListCreateView.as_view(),
        name="comment-list-create",
    ),
    path(
        "<int:pk>/",
        CommentDetailView.as_view(),
        name="comment-detail",
    ),
]