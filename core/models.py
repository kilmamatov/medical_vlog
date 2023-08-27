from django.db import models
from user_auth.models import UserModel


class TagModel(models.Model):
    name = models.CharField(max_length=30)

    class Meta:
        ordering = ("name",)
        verbose_name = "Тэг"
        verbose_name_plural = "Тэги"

    def __str__(self):
        return self.name


class PostModel(models.Model):
    user = models.ForeignKey(
        UserModel,
        verbose_name="Пользователь",
        on_delete=models.CASCADE,
    )
    title = models.CharField("Тема", max_length=255)
    text = models.TextField(verbose_name="Описание")
    photo = models.ImageField(verbose_name="Фото", blank=True, null=True)
    tags = models.ManyToManyField(TagModel, related_name="posts", blank=True)

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Список постов"

    def __str__(self):
        return self.title
