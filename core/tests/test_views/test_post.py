from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from core import factories
from core.models import PostModel


class PostViewSetTestCase(TestCase):
    def setUp(self):
        self.user = factories.User()
        self.client = APIClient()
        self.post = factories.Post(user=self.user)
        self.client.force_authenticate(user=self.user)

    def test_list_post(self):
        """
        Получаем список post
        """
        url = reverse("core:post-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(response.data),
            PostModel.objects.count(),
            msg="Сверяем количество созданных постов",
        )

    def test_create_post(self):
        """
        Создание post
        """
        url = reverse("core:post-list")
        data = {"title": self.post.title, "text": self.post.text}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            PostModel.objects.filter(title=data["title"]).first().title,
            response.data["title"],
            msg="Сверяем title из БД и тела запроса",
        )

    def test_retrieve_post(self):
        """
        Получение определенного post
        """
        post = self.post
        url = reverse("core:post-detail", kwargs={"slug": post.slug})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["slug"],
            post.slug,
            msg="Сверяем slug из ответа и базы",
        )

    def test_patch_post(self):
        """
        Частичное Обновление post
        """
        post = self.post
        url = reverse("core:post-detail", kwargs={"slug": post.slug})
        data = {"title": "Updated Tag"}
        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        post.refresh_from_db()
        self.assertEqual(
            post.title,
            data["title"],
            msg="Сравниваем обновленные данные c отправляемыми",
        )

    def test_put_post(self):
        """
        Обновление post
        """
        post = self.post
        url = reverse("core:post-detail", kwargs={"slug": post.slug})
        data = {"title": "Updated Tag", "text": "Updated text"}
        response = self.client.put(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        post.refresh_from_db()
        self.assertEqual(
            post.title,
            data["title"],
            msg="Сравниваем обновленные данные c отправляемыми",
        )

    def test_delete_tag(self):
        """
        Удаление post
        """
        post = self.post
        url = reverse("core:post-detail", kwargs={"slug": post.slug})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(
            PostModel.objects.filter(slug=post.slug).exists(),
            False,
            msg="Проверяем на наличие в бд",
        )
