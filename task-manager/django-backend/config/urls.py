from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/accounts/", include("accounts.urls")),
    path("api/projects/", include("project_management.urls")),
    path("api/tasks/", include("task_management.urls")),
    path("api/comments/", include("comments.urls")),
    path("api/notifications/", include("notifications.urls")),
]