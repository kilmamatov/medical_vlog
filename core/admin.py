from django.contrib import admin
from .models import UserProfile
from .models import Post
from .models import Tag


@admin.register(UserProfile)
class UserProfile(admin.ModelAdmin):
    list_display = ('nickname',)


@admin.register(Post)
class Post(admin.ModelAdmin):
    list_display = ('title',)


@admin.register(Tag)
class Tags(admin.ModelAdmin):
    list_display = ('name',)

