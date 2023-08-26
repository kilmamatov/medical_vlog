from rest_framework import serializers

from user_auth.models import UserModel
from core.models import TagModel, PostModel


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = TagModel
        fields = "__all__"


class PostSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, required=False)

    class Meta:
        model = PostModel
        exclude = ("user",)

    def create(self, validated_data):
        user = self.context["request"].user
        user_profile = UserModel.objects.filter(user=user).first()
        validated_data["user"] = user_profile
        return super().create(validated_data)


class UserProfile(serializers.ModelSerializer):
    post = PostSerializer

    class Meta:
        model = UserModel
        fields = ("username",)
