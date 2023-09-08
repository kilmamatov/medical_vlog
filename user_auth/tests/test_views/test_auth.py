from unittest import TestCase

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from core import factories
from user_auth.models import UserModel


class AuthUserTestCase(TestCase):
    def setUp(self):
        self.user = factories.User()
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_registration_user(self):
        url = reverse("user_auth:registration")
        data = {
            "username": "string",
            "password": "stringst",
            "password_again": "stringst",
            "email": "striasdngsdafasdf@mail.ru",
        }
        response = self.client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert (
            UserModel.objects.get(username=data["username"]).username
            == data["username"]
        )

    def test_update_info_user(self):
        url = reverse("user_auth:profile", args={self.user.pk})
        data = {
            "username": "updatename",
            "description": "updatedescrip",
        }
        response = self.client.patch(url, data)
        assert response.status_code == status.HTTP_200_OK
        assert (
            UserModel.objects.get(username=data["username"]).username
            == data["username"]
        )
        assert (
            UserModel.objects.get(username=data["username"]).description
            == data["description"]
        )

    def test_bad_update_info_user(self):
        url = reverse("user_auth:profile", args={self.user.pk + 1})
        data = {
            "username": "updatename",
            "description": "updatedescrip",
        }
        response = self.client.patch(url, data)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json()["message"] == "User does not exist, try again"

    def test_delete_user(self):
        url = reverse("user_auth:profile", args={self.user.pk})
        response = self.client.delete(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["message"] == "User successfully deleted"

    def test_bad_delete_user(self):
        url = reverse("user_auth:profile", args={self.user.pk + 1})
        response = self.client.delete(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json()["message"] == "User does not exist, try again"
