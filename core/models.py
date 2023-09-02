from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType

from core.utils import random_string
from user_auth.models import UserModel


class TagModel(models.Model):
    name = models.CharField(max_length=30)

    class Meta:
        ordering = ("name",)
        verbose_name = "Тэг"
        verbose_name_plural = "Тэги"

    def __str__(self):
        return self.name


class LikeModel(models.Model):
    user = models.ForeignKey(
        UserModel,
        verbose_name="Пользователь",
        on_delete=models.CASCADE,
    )
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")


class PostModel(models.Model):
    user = models.ForeignKey(
        UserModel,
        verbose_name="Пользователь",
        on_delete=models.CASCADE,
    )
    title = models.CharField("Тема", max_length=255)
    text = models.TextField(verbose_name="Описание")
    photo = models.ImageField(
        verbose_name="Фотография",
        blank=True,
        null=True,
        upload_to="static/",
    )
    tags = models.ManyToManyField(TagModel, related_name="posts", blank=True)
    slug = models.SlugField(unique=True, blank=True)
    likes = GenericRelation(LikeModel)
    created_at = models.DateTimeField(verbose_name="Время создания", auto_now_add=True)

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Список постов"

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = slugify(f"{random_string()}")
            while PostModel.objects.filter(slug=slug).exists():
                slug = slugify(f"{random_string()}")
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("post", args=[str(self.slug)])

    @property
    def total_likes(self):
        return self.likes.count()

    @property
    def total_comment(self):
        return self.comments.count()

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
    photo = models.ImageField(
        verbose_name="Фотография",
        blank=True,
        null=True,
        upload_to="static/",
    )
    text = models.TextField(verbose_name="Текст комментария")
    likes = GenericRelation(LikeModel)
    created_at = models.DateTimeField(verbose_name="Время создания", auto_now=True)

    class Meta:
        ordering = ("created_at",)
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

    @property
    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return f"{self.user.username} - {self.post.title}"
