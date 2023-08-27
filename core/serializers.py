from rest_framework import serializers

from core.models import PostModel, TagModel
from user_auth.models import UserModel


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = TagModel
        fields = "__all__"


class PostSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, required=False)

    class Meta:
        model = PostModel
        exclude = ("user",)


# class UserProfile(serializers.ModelSerializer):
#     post = PostSerializer
#
#     class Meta:
#         model = UserModel
#         fields = ("username",)
