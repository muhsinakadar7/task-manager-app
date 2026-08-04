from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


class AccountAPITestCase(APITestCase):

    def setUp(self):
        """
        Create a test user.
        """

        self.user = User.objects.create_user(
            username="john",
            email="john@example.com",
            password="Password@123"
        )

    def test_register_user(self):
        """
        Test user registration.
        """

        url = reverse("accounts:register")

        data = {
            "username": "mike",
            "first_name": "Mike",
            "last_name": "Smith",
            "email": "mike@example.com",
            "phone_number": "9876543210",
            "password": "Password@123",
            "confirm_password": "Password@123"
        }

        response = self.client.post(url, data)

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

    def test_login_user(self):
        """
        Test login API.
        """

        url = reverse("accounts:login")

        data = {
            "username": "john",
            "password": "Password@123"
        }

        response = self.client.post(url, data)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_invalid_login(self):
        """
        Invalid password should fail.
        """

        url = reverse("accounts:login")

        response = self.client.post(
            url,
            {
                "username": "john",
                "password": "WrongPassword"
            }
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_get_profile(self):
        """
        Retrieve authenticated user's profile.
        """

        self.client.force_authenticate(user=self.user)

        url = reverse("accounts:profile")

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_profile_requires_authentication(self):
        """
        Anonymous users cannot access profile.
        """

        url = reverse("accounts:profile")

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )