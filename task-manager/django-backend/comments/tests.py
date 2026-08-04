from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from comments.models import Comment
from project_management.models import Project, ProjectMember
from task_management.models import Task

User = get_user_model()


class CommentAPITestCase(APITestCase):
    """
    Test cases for Comment APIs.
    """

    def setUp(self):
        # Create users
        self.owner = User.objects.create_user(
            username="owner",
            email="owner@example.com",
            password="password123",
        )

        self.member = User.objects.create_user(
            username="member",
            email="member@example.com",
            password="password123",
        )

        self.other_user = User.objects.create_user(
            username="other",
            email="other@example.com",
            password="password123",
        )

        # Create project
        self.project = Project.objects.create(
            name="Task Manager",
            description="Demo Project",
            owner=self.owner,
        )

        # Add member
        ProjectMember.objects.create(
            project=self.project,
            user=self.member,
            role=ProjectMember.Role.DEVELOPER,
        )

        # Create task
        self.task = Task.objects.create(
            project=self.project,
            title="Create Login API",
            description="JWT Authentication",
            assigned_to=self.member,
            priority=Task.Priority.HIGH,
            status=Task.Status.TODO,
        )

        # Create comment
        self.comment = Comment.objects.create(
            task=self.task,
            user=self.member,
            content="Initial Comment",
        )

    def test_create_comment(self):
        self.client.force_authenticate(self.member)

        url = reverse("comments:comment-list-create")

        data = {
            "task": self.task.id,
            "content": "New Comment",
        }

        response = self.client.post(url, data)

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

    def test_list_comments(self):
        self.client.force_authenticate(self.member)

        url = reverse("comments:comment-list-create")

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_get_comment(self):
        self.client.force_authenticate(self.member)

        url = reverse(
            "comments:comment-detail",
            kwargs={"pk": self.comment.id},
        )

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_update_comment(self):
        self.client.force_authenticate(self.member)

        url = reverse(
            "comments:comment-detail",
            kwargs={"pk": self.comment.id},
        )

        response = self.client.patch(
            url,
            {
                "content": "Updated Comment",
            },
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_delete_comment(self):
        self.client.force_authenticate(self.member)

        url = reverse(
            "comments:comment-detail",
            kwargs={"pk": self.comment.id},
        )

        response = self.client.delete(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )

    def test_non_member_cannot_create_comment(self):
        self.client.force_authenticate(self.other_user)

        url = reverse("comments:comment-list-create")

        response = self.client.post(
            url,
            {
                "task": self.task.id,
                "content": "Unauthorized",
            },
        )

        self.assertIn(
            response.status_code,
            [
                status.HTTP_403_FORBIDDEN,
                status.HTTP_400_BAD_REQUEST,
            ],
        )

    def test_filter_comments_by_task(self):
        self.client.force_authenticate(self.member)

        url = reverse("comments:comment-list-create")

        response = self.client.get(
            url,
            {
                "task": self.task.id,
            },
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            len(response.data),
            1,
        )