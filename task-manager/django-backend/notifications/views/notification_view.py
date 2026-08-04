from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from notifications.selectors.notification_selector import (
    NotificationSelector,
)
from notifications.serializers.notification_serializer import (
    NotificationSerializer,
)
from notifications.services.delete_notification_service import (
    DeleteNotificationService,
)
from notifications.services.mark_as_read_service import (
    MarkAsReadService,
)


class NotificationListView(APIView):
    """
    List notifications for the authenticated user.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        notifications = NotificationSelector.get_notifications_by_user(
            request.user
        )

        serializer = NotificationSerializer(
            notifications,
            many=True,
        )

        return Response(serializer.data)


class NotificationDetailView(APIView):
    """
    Retrieve or delete a notification.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        notification = NotificationSelector.get_notification_by_id(pk)

        if notification.recipient != request.user:
            return Response(
                {"detail": "Permission denied."},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = NotificationSerializer(notification)

        return Response(serializer.data)

    def delete(self, request, pk):
        DeleteNotificationService.execute(
            request.user,
            pk,
        )

        return Response(
            status=status.HTTP_204_NO_CONTENT,
        )


class MarkNotificationAsReadView(APIView):
    """
    Mark a single notification as read.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        notification = MarkAsReadService.execute(
            request.user,
            pk,
        )

        serializer = NotificationSerializer(notification)

        return Response(serializer.data)


class MarkAllNotificationsAsReadView(APIView):
    """
    Mark all notifications as read.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        notifications = MarkAsReadService.mark_all_as_read(
            request.user,
        )

        serializer = NotificationSerializer(
            notifications,
            many=True,
        )

        return Response(serializer.data)


class DeleteReadNotificationsView(APIView):
    """
    Delete all read notifications.
    """

    permission_classes = [IsAuthenticated]

    def delete(self, request):
        deleted_count = (
            DeleteNotificationService.delete_all_read_notifications(
                request.user,
            )
        )

        return Response(
            {
                "message": (
                    f"{deleted_count} notifications deleted successfully."
                )
            },
            status=status.HTTP_200_OK,
        )


class UnreadNotificationCountView(APIView):
    """
    Return unread notification count.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        count = NotificationSelector.count_unread_notifications(
            request.user,
        )

        return Response(
            {
                "unread_count": count,
            }
        )