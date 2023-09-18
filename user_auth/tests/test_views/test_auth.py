from datetime import datetime, timedelta
from unittest import TestCase

from django.urls import reverse
from rest_framework import serializers, status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
import pytest
from core import factories
from user_auth.models import UserModel
from user_auth.serializers import RegisterUser


class AuthUserTestCase(TestCase):
    def setUp(self):
        self.user = factories.User()
        self.user2 = factories.User()
        self.client = APIClient()
        self.client2 = APIClient()
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

    def test_registration_user_bad_password(self):
        url = reverse("user_auth:registration")
        data = {
            "username": "string",
            "password": "stringst123",
            "password_again": "stringst",
            "email": "striasdngsdafasdf@mail.ru",
        }
        response = self.client.post(url, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_registration_user_bad_username(self):
        url = reverse("user_auth:registration")
        data = {
            "username": self.user.username,
            "password": "stringst",
            "password_again": "stringst",
            "email": "striasdngsdafasdf@mail.ru",
        }
        response = self.client.post(url, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_bad_credentials_registration_user(self):
        url = reverse("user_auth:registration")
        data = {
            "username": "",
            "password": "stringst",
            "password_again": "stringst",
            "email": "",
        }
        response = self.client.post(url, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

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

    def test_bad_pk_update_info_user(self):
        url = reverse("user_auth:profile", args={self.user.pk + 120})
        data = {
            "username": "updatename",
            "description": "updatedescrip",
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        assert response.json()["message"] == "User does not exist, try again"

    def test_bad_request_pk_update_info_user(self):
        url = reverse("user_auth:profile", args={self.user2.pk})
        data = {
            "username": "updatename",
            "description": "updatedescrip",
        }
        response = self.client.patch(url, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json()["message"] == "User does have permission for changed"

    def test_delete_user(self):
        url = reverse("user_auth:profile", args={self.user.pk})
        response = self.client.delete(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["message"] == "User successfully deleted"

    def test_bad_delete_user(self):
        url = reverse("user_auth:profile", args={self.user.pk + 120})
        response = self.client.delete(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json()["message"] == "User does not exist, try again"

    def test_passwords_match(self):
        data = {
            "username": "user",
            "password": "password123",
            "password_again": "password123",
            "email": "avd@mail.ru",
        }
        serializer = RegisterUser(data=data)
        assert serializer.is_valid()

    def test_passwords_do_not_match(self):
        data = {
            "username": "user",
            "password": "password123",
            "password_again": "avdsvssadf",
            "email": "avd@mail.ru",
        }
        with pytest.raises(serializers.ValidationError, match="Пароли не совпадают"):
            serializer = RegisterUser(data=data)
            serializer.is_valid(raise_exception=True)

    def test_question_serializer_fail(self):
        data = {
            "username": "user",
            "password": "password123",
            "password_again": "avdsvszxvxcz",
            "email": "avd@mail.ru",
        }
        with pytest.raises(serializers.ValidationError, match="Пароли не совпадают"):
            serializer = RegisterUser(data=data)
            serializer.is_valid(raise_exception=True)

    def test_logout(self):
        url = reverse("user_auth:logout")
        user_token = RefreshToken.for_user(self.user)
        data = {
            "refresh_token": str(user_token),
        }
        response = self.client.post(url, data)
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_verify_email(self):
        token = RefreshToken.for_user(self.user)
        url = reverse("user_auth:email-verify") + "?token=" + str(token)
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"email": "Successfully activated"}

    def test_bad_verify_email(self):
        token = RefreshToken.for_user(self.user)
        url = reverse("user_auth:email-verify") + "?token=" + str(token) + "asdasd"
        response = self.client.get(url)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {"error": "Invalid token"}
        user = UserModel.objects.get(id=self.user.id)
        assert not user.is_verify_email
        assert not user.is_active

    def test_bad_verify_email_expired_token(self):
        token = RefreshToken.for_user(self.user).access_token
        token.set_exp(from_time=datetime.utcnow(), lifetime=timedelta(hours=-25))
        url = reverse("user_auth:email-verify") + "?token=" + str(token)
        response = self.client.get(url)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data == {"error": "Activation Expired"}
        user = UserModel.objects.get(id=self.user.id)
        assert not user.is_verify_email
        assert not user.is_active
