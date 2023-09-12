from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from core import factories


class PostLikeMixinTestCase(TestCase):
    def setUp(self):
        self.user = factories.User()
        self.client = APIClient()
        self.post = factories.Post(user=self.user)
        self.client.force_authenticate(user=self.user)
        self.user2 = factories.User()
        self.client2 = APIClient()
        self.client2.force_authenticate(user=self.user2)

    def test_like_post(self):
        """
        лайкаем пост
        """
        post = self.post
        url = reverse("core:post-like-post", kwargs={"slug": post.slug})
        response = self.client.post(url)
        assert response.status_code == status.HTTP_200_OK
        assert post.total_likes == 1, "Проверяем лайк"

        url = reverse("core:post-like-post", kwargs={"slug": post.slug})
        response = self.client2.post(url)
        assert response.status_code == status.HTTP_200_OK

        assert post.total_likes == 2, "Проверяем лайк от другого пользователя"

    def test_unlike_post(self):
        """
        убираем лайк c поста
        """
        post = self.post
        url = reverse("core:post-like-post", kwargs={"slug": post.slug})
        response = self.client.post(url)
        assert response.status_code == status.HTTP_200_OK
        assert post.total_likes == 1, "ставим лайк"

        url = reverse("core:post-unlike-post", kwargs={"slug": post.slug})
        response = self.client.post(url)
        assert response.status_code == status.HTTP_200_OK
        assert post.total_likes == 0, "убираем лайк"


class CommentLikeMixinTestCase(TestCase):
    def setUp(self):
        self.user = factories.User()
        self.client = APIClient()
        self.post = factories.Post(user=self.user)
        self.comment = factories.Comment(user=self.user, post=self.post)
        self.client.force_authenticate(user=self.user)
        self.user2 = factories.User()
        self.client2 = APIClient()
        self.client2.force_authenticate(user=self.user2)

    def test_like_comment(self):
        """
        лайкаем comment
        """
        post = self.post
        comment = self.comment
        url = reverse(
            "core:comment-like-comment",
            kwargs={"slug": post.slug, "pk": comment.id},
        )
        response = self.client.post(url)
        assert response.status_code == status.HTTP_200_OK
        assert comment.total_likes == 1, "Проверяем лайк"

        url = reverse(
            "core:comment-like-comment",
            kwargs={"slug": post.slug, "pk": comment.id},
        )
        response = self.client2.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            comment.total_likes,
            2,
            msg="Проверяем лайк от другого пользователя",
        )

    def test_unlike_comment(self):
        """
        Убираем лайк c comment
        """
        post = self.post
        comment = self.comment
        url = reverse(
            "core:comment-like-comment",
            kwargs={"slug": post.slug, "pk": comment.id},
        )
        response = self.client.post(url)
        assert response.status_code == status.HTTP_200_OK
        assert comment.total_likes == 1, "ставим лайк"

        url = reverse(
            "core:comment-unlike-comment",
            kwargs={"slug": post.slug, "pk": comment.id},
        )
        response = self.client.post(url)
        assert response.status_code == status.HTTP_200_OK
        assert comment.total_likes == 0, "убираем лайк"
