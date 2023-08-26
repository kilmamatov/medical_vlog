from django.contrib import admin

from core.models import PostModel, TagModel
from user_auth.models import UserModel


@admin.register(UserModel)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username",)


@admin.register(PostModel)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title",)


@admin.register(TagModel)
class TagsAdmin(admin.ModelAdmin):
    list_display = ("name",)
