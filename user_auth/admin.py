from django.contrib import admin

from user_auth.models import UserModel


@admin.register(UserModel)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username",)
