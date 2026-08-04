from django.urls import path

from project_management.views.member_view import (
    AddProjectMemberView,
    ProjectMemberListView,
    RemoveProjectMemberView,
)
from project_management.views.project_view import (
    ProjectDetailView,
    ProjectListCreateView,
)

app_name = "project_management"

urlpatterns = [
    # Project APIs
    path(
        "",
        ProjectListCreateView.as_view(),
        name="project-list-create",
    ),
    path(
        "<int:project_id>/",
        ProjectDetailView.as_view(),
        name="project-detail",
    ),

    # Project Member APIs
    path(
        "<int:project_id>/members/",
        ProjectMemberListView.as_view(),
        name="member-list",
    ),
    path(
        "<int:project_id>/members/add/",
        AddProjectMemberView.as_view(),
        name="member-add",
    ),
    path(
        "<int:project_id>/members/<int:user_id>/",
        RemoveProjectMemberView.as_view(),
        name="member-remove",
    ),
]