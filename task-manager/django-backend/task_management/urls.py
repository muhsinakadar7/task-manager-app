from django.urls import path

from task_management.views.report_view import (
    CompletedTaskListView,
    HighPriorityTaskListView,
    OverdueTaskListView,
    TaskSummaryView,
    TasksByProjectView,
    TasksByUserView,
)

from task_management.views.task_view import (
    AssignTaskView,
    ChangeStatusView,
    TaskDetailView,
    TaskListCreateView,
)

app_name = "task_management"

urlpatterns = [
    # Task CRUD
    path(
        "",
        TaskListCreateView.as_view(),
        name="task-list-create",
    ),
    path(
        "<int:pk>/",
        TaskDetailView.as_view(),
        name="task-detail",
    ),

    # Assignment
    path(
        "<int:pk>/assign/",
        AssignTaskView.as_view(),
        name="assign-task",
    ),

    # Status
    path(
        "<int:pk>/status/",
        ChangeStatusView.as_view(),
        name="change-status",
    ),

    # Reports
    path(
        "summary/",
        TaskSummaryView.as_view(),
        name="task-summary",
    ),
    path(
        "completed/",
        CompletedTaskListView.as_view(),
        name="completed-tasks",
    ),
    path(
        "overdue/",
        OverdueTaskListView.as_view(),
        name="overdue-tasks",
    ),
    path(
        "high-priority/",
        HighPriorityTaskListView.as_view(),
        name="high-priority-tasks",
    ),
    path(
        "project-report/",
        TasksByProjectView.as_view(),
        name="project-report",
    ),
    path(
        "user-report/",
        TasksByUserView.as_view(),
        name="user-report",
    ),
]