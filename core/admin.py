from django.contrib import admin

from core.models import CommentModel, PostModel, TagModel


class CommentInline(admin.TabularInline):
    model = CommentModel
    extra = 1


@admin.register(PostModel)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "total_likes", "total_comment")
    readonly_fields = ("slug",)
    inlines = [CommentInline]


@admin.register(TagModel)
class TagsAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(CommentModel)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("user", "total_likes", "created_at")
