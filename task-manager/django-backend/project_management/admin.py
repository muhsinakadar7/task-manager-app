from django.contrib import admin

from .models import Project, ProjectMember


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    """
    Admin configuration for Project model.
    """

    list_display = (
        "id",
        "name",
        "owner",
        "status",
        "start_date",
        "end_date",
        "created_at",
    )

    list_filter = (
        "status",
        "created_at",
    )

    search_fields = (
        "name",
        "owner__username",
        "owner__email",
    )

    ordering = (
        "-created_at",
    )


@admin.register(ProjectMember)
class ProjectMemberAdmin(admin.ModelAdmin):
    """
    Admin configuration for ProjectMember model.
    """

    list_display = (
        "id",
        "project",
        "user",
        "role",
        "joined_at",
    )

    list_filter = (
        "role",
    )

    search_fields = (
        "project__name",
        "user__username",
        "user__email",
    )

    ordering = (
        "-joined_at",
    )