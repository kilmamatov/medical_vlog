from django.contrib import admin

from core.models import PostModel, TagModel


@admin.register(PostModel)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title",)


@admin.register(TagModel)
class TagsAdmin(admin.ModelAdmin):
    list_display = ("name",)
