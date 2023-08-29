import uuid
from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from core.utils import translate_word
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
    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Список постов"

    def save(self, *args, **kwargs):
        if not self.slug:
            title = translate_word(self.title)
            self.slug = slugify(f"{self.user.username}//{title}")
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("post", args=[str(self.slug)])

    def __str__(self):
        return self.title


class CommentModel(models.Model):
    user = models.ForeignKey(
        UserModel,
        verbose_name="Пользователь",
        on_delete=models.CASCADE,
    )
    post = models.ForeignKey(
        PostModel,
        verbose_name="Пост",
        on_delete=models.CASCADE,
        related_name="comments",
    )
    text = models.TextField(verbose_name="Текст комментария")
    created_at = models.DateTimeField(verbose_name="Время создания", auto_now_add=True)

    class Meta:
        ordering = ("created_at",)
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

    def __str__(self):
        return f"{self.user.username} - {self.post.title}"
