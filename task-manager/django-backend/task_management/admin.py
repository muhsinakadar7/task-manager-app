from django.contrib import admin

from task_management.models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """
    Admin configuration for Task model.
    """

    list_display = (
        "id",
        "title",
        "project",
        "assigned_to",
        "priority",
        "status",
        "due_date",
        "created_at",
    )

    list_filter = (
        "priority",
        "status",
        "project",
        "created_at",
    )

    search_fields = (
        "title",
        "description",
        "assigned_to__username",
        "project__name",
    )

    ordering = (
        "-created_at",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )