from django.db import models
from user_auth.models import User


class Tag(models.Model):
    name = models.CharField(max_length=30)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

    def __str__(self):
        return self.name


class Post(models.Model):
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    title = models.CharField('Тема', max_length=255)
    text = models.TextField(verbose_name='Описание')
    photo = models.ImageField(verbose_name='Фото', blank=True, null=True)
    tags = models.ManyToManyField(Tag, related_name='posts')

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Список постов'

    def __str__(self):
        return self.title


class UserBlog(models.Model):
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    nickname = models.CharField(verbose_name='Никнейм', max_length=20, unique=True)
    photo = models.ImageField(verbose_name='Фотография', blank=True, null=True)
    description = models.TextField(verbose_name='Описание', blank=True)

    class Meta:
        ordering = ('nickname',)
        verbose_name = 'Профиль'
        verbose_name_plural = 'Список профилей'

    def __str__(self):
        return self.nickname


