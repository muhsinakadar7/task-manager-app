from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from notifications.models import Notification

User = get_user_model()


class NotificationAPITestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="john",
            email="john@example.com",
            password="password123",
        )

        self.other_user = User.objects.create_user(
            username="alice",
            email="alice@example.com",
            password="password123",
        )

        self.notification = Notification.objects.create(
            recipient=self.user,
            title="Task Assigned",
            message="You have been assigned a task.",
            notification_type=Notification.NotificationType.TASK_ASSIGNED,
        )

    def test_list_notifications(self):
        self.client.force_authenticate(self.user)

        url = reverse("notifications:notification-list")

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_notification_detail(self):
        self.client.force_authenticate(self.user)

        url = reverse(
            "notifications:notification-detail",
            kwargs={
                "pk": self.notification.id
            },
        )

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_mark_notification_as_read(self):
        self.client.force_authenticate(self.user)

        url = reverse(
            "notifications:notification-mark-read",
            kwargs={
                "pk": self.notification.id
            },
        )

        response = self.client.post(url)

        self.notification.refresh_from_db()

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertTrue(
            self.notification.is_read
        )

    def test_mark_all_notifications_as_read(self):
        self.client.force_authenticate(self.user)

        Notification.objects.create(
            recipient=self.user,
            title="Task Updated",
            message="Task updated",
            notification_type=Notification.NotificationType.TASK_UPDATED,
        )

        url = reverse(
            "notifications:notification-read-all"
        )

        response = self.client.post(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            Notification.objects.filter(
                recipient=self.user,
                is_read=False,
            ).count(),
            0,
        )

    def test_delete_notification(self):
        self.client.force_authenticate(self.user)

        url = reverse(
            "notifications:notification-detail",
            kwargs={
                "pk": self.notification.id
            },
        )

        response = self.client.delete(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )

    def test_unread_notification_count(self):
        self.client.force_authenticate(self.user)

        url = reverse(
            "notifications:notification-unread-count"
        )

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["unread_count"],
            1,
        )

    def test_other_user_cannot_access_notification(self):
        self.client.force_authenticate(
            self.other_user
        )

        url = reverse(
            "notifications:notification-detail",
            kwargs={
                "pk": self.notification.id
            },
        )

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )