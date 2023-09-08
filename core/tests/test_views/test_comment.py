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
        self.client = APIClient()
        self.comment = factories.Comment(user=self.user, post=self.post)
        self.client.force_authenticate(user=self.user)

    def test_list_comment(self):
        """
        Получаем список comment
        """
        url = reverse("core:comment-list", kwargs={"slug": self.post.slug})
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == CommentModel.objects.count(), "Сверяем количество созданных постов"

    def test_create_comment(self):
        """
        Создание comment
        """
        url = reverse("core:comment-list", kwargs={"slug": self.post.slug})
        data = {
            "text": self.comment.text,
        }
        response = self.client.post(url, data)

        assert response.status_code == status.HTTP_201_CREATED
        self.assertEqual(
            CommentModel.objects.filter(text=data["text"])
            .first()
            .text,  # нужно сделать более сложный алгоритм
            response.data["text"],
            msg="Сверяем text из БД и тела запроса",
        )

    # def test_retrieve_post(self):
    #     """
    #     Получение определенного post
    #     """
    #     post = self.post
    #     url = reverse('core:post-detail', kwargs={'slug': post.slug})
    #     response = self.client.get(url)
    #
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(response.data["slug"], post.slug, msg='Сверяем slug из ответа и базы')
