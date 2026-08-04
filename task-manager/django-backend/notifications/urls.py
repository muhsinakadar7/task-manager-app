from django.urls import path

from notifications.views.notification_view import (
    DeleteReadNotificationsView,
    MarkAllNotificationsAsReadView,
    MarkNotificationAsReadView,
    NotificationDetailView,
    NotificationListView,
    UnreadNotificationCountView,
)

app_name = "notifications"

urlpatterns = [
    path(
        "",
        NotificationListView.as_view(),
        name="notification-list",
    ),

    path(
        "<int:pk>/",
        NotificationDetailView.as_view(),
        name="notification-detail",
    ),

    path(
        "<int:pk>/read/",
        MarkNotificationAsReadView.as_view(),
        name="notification-mark-read",
    ),

    path(
        "read-all/",
        MarkAllNotificationsAsReadView.as_view(),
        name="notification-read-all",
    ),

    path(
        "delete-read/",
        DeleteReadNotificationsView.as_view(),
        name="notification-delete-read",
    ),

    path(
        "unread-count/",
        UnreadNotificationCountView.as_view(),
        name="notification-unread-count",
    ),
]