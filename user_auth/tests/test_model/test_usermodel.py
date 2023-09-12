from django.test import TestCase

from user_auth.models import UserModel


class UserTestCase(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(
            username="testname",
            email="test@mail.ru",
            password="testpass",
        )
        self.super_user = UserModel.objects.create_superuser(
            username="supertestname",
            email="supertest@mail.ru",
            password="supertestpass",
        )

    def test_create_user(self):
        assert self.user == UserModel.objects.get(username="testname")
        assert self.user.email == UserModel.objects.get(email="test@mail.ru").email
        assert self.user.username == UserModel.objects.get(username="testname").username

    def test_create_super_user(self):
        assert self.super_user == UserModel.objects.get(username="supertestname")
        assert (
            self.super_user.email
            == UserModel.objects.get(email="supertest@mail.ru").email
        )
        assert (
            self.super_user.username
            == UserModel.objects.get(username="supertestname").username
        )

    def test_str_user(self):
        assert UserModel.__str__(self.user) == self.user.username
