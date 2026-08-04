from django.test import TestCase

# Create your tests here.
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from project_management.models import Project, ProjectMember
from task_management.models import Task

User = get_user_model()


class TaskAPITestCase(APITestCase):
    """
    Test cases for Task APIs.
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

        # Create project
        self.project = Project.objects.create(
            name="Task Manager",
            description="Demo Project",
            owner=self.owner,
        )

        # Add member to project
        ProjectMember.objects.create(
            project=self.project,
            user=self.member,
            role=ProjectMember.Role.DEVELOPER,
        )

        # Create task
        self.task = Task.objects.create(
            project=self.project,
            title="Create Login API",
            description="Implement JWT authentication",
            assigned_to=self.member,
            priority=Task.Priority.HIGH,
            status=Task.Status.TODO,
        )

    def test_create_task(self):
        """
        Test task creation.
        """
        self.client.force_authenticate(user=self.owner)

        url = reverse("task_management:task-list-create")

        data = {
            "project": self.project.id,
            "title": "Create Dashboard",
            "description": "Dashboard module",
            "assigned_to": self.member.id,
            "priority": Task.Priority.MEDIUM,
            "status": Task.Status.TODO,
        }

        response = self.client.post(url, data)

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

    def test_get_tasks(self):
        """
        Test retrieving all tasks.
        """
        self.client.force_authenticate(user=self.owner)

        url = reverse("task_management:task-list-create")

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_get_task_detail(self):
        """
        Test retrieving a single task.
        """
        self.client.force_authenticate(user=self.owner)

        url = reverse(
            "task_management:task-detail",
            kwargs={"pk": self.task.id},
        )

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_update_task(self):
        """
        Test updating a task.
        """
        self.client.force_authenticate(user=self.owner)

        url = reverse(
            "task_management:task-detail",
            kwargs={"pk": self.task.id},
        )

        data = {
            "title": "Updated Login API",
            "priority": Task.Priority.LOW,
        }

        response = self.client.patch(url, data)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_delete_task(self):
        """
        Test deleting a task.
        """
        self.client.force_authenticate(user=self.owner)

        url = reverse(
            "task_management:task-detail",
            kwargs={"pk": self.task.id},
        )

        response = self.client.delete(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )

    def test_change_status(self):
        """
        Test changing task status.
        """
        self.client.force_authenticate(user=self.owner)

        url = reverse(
            "task_management:change-status",
            kwargs={"pk": self.task.id},
        )

        response = self.client.patch(
            url,
            {
                "status": Task.Status.COMPLETED,
            },
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_assign_task(self):
        """
        Test assigning a task.
        """
        self.client.force_authenticate(user=self.owner)

        url = reverse(
            "task_management:assign-task",
            kwargs={"pk": self.task.id},
        )

        response = self.client.post(
            url,
            {
                "assigned_to": self.member.id,
            },
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )