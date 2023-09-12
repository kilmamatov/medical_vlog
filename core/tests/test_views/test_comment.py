from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from core import factories
from core.models import CommentModel


class CommentViewSetTestCase(TestCase):
    def setUp(self):
        self.user = factories.User()
        self.post = factories.Post(user=self.user)
        self.post2 = factories.Post(user=self.user)
        self.comment = factories.Comment(user=self.user, post=self.post)
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_list_comment(self):
        """
        Получаем список comment
        """
        url = reverse("core:comment-list", kwargs={"slug": self.post.slug})
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert (
            len(response.data) == CommentModel.objects.count()
        ), "Сверяем количество созданных comment"

    def test_create_comment(self):  # переделать
        """
        Создание comment
        """
        post = self.post2
        url = reverse("core:comment-list", kwargs={"slug": post.slug})
        data = {
            "text": self.comment.text,
        }
        response = self.client.post(url, data)

        assert response.status_code == status.HTTP_201_CREATED
        assert (
            post.total_comment == 1
        ), "Проверяем количество созданных комментов к посту"
        assert (
            CommentModel.objects.filter(text=data["text"]).first().text
            == response.data["text"]
        ), "Сверяем text из БД и тела запроса"

    def test_retrieve_comment(self):
        """
        Получение определенного comment
        """
        post = self.post
        comment = self.comment
        url = reverse(
            "core:comment-detail",
            kwargs={"slug": post.slug, "pk": comment.id},
        )
        response = self.client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["text"] == comment.text, "Сверяем text из ответа и базы"

    def test_patch_comment(self):
        """
        Частичное Обновление comment
        """
        post = self.post
        comment = self.comment
        url = reverse(
            "core:comment-detail",
            kwargs={"slug": post.slug, "pk": comment.id},
        )
        data = {"text": "Updated comment"}
        response = self.client.patch(url, data)

        assert response.status_code == status.HTTP_200_OK
        comment.refresh_from_db()
        assert (
            comment.text == data["text"]
        ), "Сравниваем обновленные данные c отправляемыми"

    def test_put_comment(self):
        """
        Обновление comment
        """
        post = self.post
        comment = self.comment
        url = reverse(
            "core:comment-detail",
            kwargs={"slug": post.slug, "pk": comment.id},
        )
        data = {"text": "Updated text comment"}
        response = self.client.put(url, data)

        assert response.status_code == status.HTTP_200_OK
        comment.refresh_from_db()
        assert (
            comment.text == data["text"]
        ), "Сравниваем обновленные данные c отправляемыми"

    def test_delete_tag(self):
        """
        Удаление comment
        """
        post = self.post
        comment = self.comment
        url = reverse(
            "core:comment-detail",
            kwargs={"slug": post.slug, "pk": comment.id},
        )
        response = self.client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert (
            CommentModel.objects.filter(id=comment.id).exists() is False
        ), "Проверяем на наличие в бд"
