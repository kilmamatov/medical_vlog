from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from core import factories
from core.models import TagModel


class TagViewSetTestCase(TestCase):
    def setUp(self):
        self.user = factories.User()
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.tag = factories.Tag()

    def test_list_tags(self):
        """
        Получаем список тегов
        """
        url = reverse("core:tag-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(response.data),
            TagModel.objects.count(),
            msg="Сверяем количество созданных тэгов",
        )

    def test_create_tag(self):
        """
        Создание тега
        """
        url = reverse("core:tag-list")
        data = {"name": "New Tag"}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response.data["name"],
            data["name"],
            msg="Сверяем name из ответа и тела запроса",
        )

    def test_retrieve_tag(self):
        """
        Получение определенного тега
        """
        tag = self.tag
        url = reverse("core:tag-detail", args=[tag.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], tag.id, msg="Сверяем id из ответа и базы")

    def test_update_tag(self):
        """
        Обновление тега
        """
        tag = self.tag
        url = reverse("core:tag-detail", args=[tag.id])
        data = {"name": "Updated Tag"}
        response = self.client.put(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        tag.refresh_from_db()
        self.assertEqual(
            tag.name, data["name"], msg="Сравниваем обновленные данные c отправляемыми"
        )

    def test_delete_tag(self):
        """
        Удаление тега
        """
        tag = self.tag
        url = reverse("core:tag-detail", args=[tag.id])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(
            TagModel.objects.filter(id=tag.id).exists(),
            False,
            msg="Проверяем на наличие в бд",
        )
