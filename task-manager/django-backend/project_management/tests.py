from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from project_management.models import Project, ProjectMember

User = get_user_model()


class ProjectManagementAPITestCase(APITestCase):
    """
    Test cases for Project Management APIs.
    """

    def setUp(self):
        self.owner = User.objects.create_user(
            username="owner",
            email="owner@example.com",
            password="Password@123"
        )

        self.member = User.objects.create_user(
            username="member",
            email="member@example.com",
            password="Password@123"
        )

        self.project = Project.objects.create(
            name="Task Manager",
            description="Project Description",
            owner=self.owner,
            status="ACTIVE"
        )

        ProjectMember.objects.create(
            project=self.project,
            user=self.owner,
            role="MANAGER"
        )

    def test_create_project(self):
        self.client.force_authenticate(user=self.owner)

        url = reverse("project_management:project-list-create")

        data = {
            "name": "CRM System",
            "description": "CRM Project",
            "status": "ACTIVE"
        }

        response = self.client.post(url, data)

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

    def test_list_projects(self):
        self.client.force_authenticate(user=self.owner)

        url = reverse("project_management:project-list-create")

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_update_project(self):
        self.client.force_authenticate(user=self.owner)

        url = reverse(
            "project_management:project-detail",
            kwargs={"project_id": self.project.id}
        )

        response = self.client.put(
            url,
            {
                "name": "Updated Project",
                "description": "Updated Description",
                "status": "COMPLETED"
            }
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_delete_project(self):
        self.client.force_authenticate(user=self.owner)

        url = reverse(
            "project_management:project-detail",
            kwargs={"project_id": self.project.id}
        )

        response = self.client.delete(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

    def test_add_member(self):
        self.client.force_authenticate(user=self.owner)

        url = reverse(
            "project_management:member-add",
            kwargs={"project_id": self.project.id}
        )

        response = self.client.post(
            url,
            {
                "user": self.member.id,
                "role": "DEVELOPER"
            }
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

    def test_remove_member(self):
        ProjectMember.objects.create(
            project=self.project,
            user=self.member,
            role="DEVELOPER"
        )

        self.client.force_authenticate(user=self.owner)

        url = reverse(
            "project_management:member-remove",
            kwargs={
                "project_id": self.project.id,
                "user_id": self.member.id
            }
        )

        response = self.client.delete(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

    def test_unauthorized_access(self):
        url = reverse("project_management:project-list-create")

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )