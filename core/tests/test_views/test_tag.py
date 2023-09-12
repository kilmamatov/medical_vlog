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
        assert response.status_code == status.HTTP_200_OK
        assert (
            len(response.data) == TagModel.objects.count()
        ), "Сверяем количество созданных тэгов"

    def test_create_tag(self):
        """
        Создание тега
        """
        url = reverse("core:tag-list")
        data = {"name": "New Tag"}
        response = self.client.post(url, data)

        assert response.status_code == status.HTTP_201_CREATED
        assert (
            response.data["name"] == data["name"]
        ), "Сверяем name из ответа и тела запроса"

    def test_retrieve_tag(self):
        """
        Получение определенного тега
        """
        tag = self.tag
        url = reverse("core:tag-detail", args=[tag.id])
        response = self.client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == tag.id, "Сверяем id из ответа и базы"

    def test_update_tag(self):
        """
        Обновление тега
        """
        tag = self.tag
        url = reverse("core:tag-detail", args=[tag.id])
        data = {"name": "Updated Tag"}
        response = self.client.put(url, data)

        assert response.status_code == status.HTTP_200_OK
        tag.refresh_from_db()
        assert tag.name == data["name"], "Сравниваем обновленные данные c отправляемыми"

    def test_delete_tag(self):
        """
        Удаление тега
        """
        tag = self.tag
        url = reverse("core:tag-detail", args=[tag.id])
        response = self.client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert (
            TagModel.objects.filter(id=tag.id).exists() is False
        ), "Проверяем на наличие в бд"
