from django.contrib import admin

from core.models import Post, Tag
from user_auth.models import UserModel


@admin.register(UserModel)
class UserModel(admin.ModelAdmin):
    list_display = ('username',)


@admin.register(Post)
class Post(admin.ModelAdmin):
    list_display = ('title',)


@admin.register(Tag)
class Tags(admin.ModelAdmin):
    list_display = ('name',)
