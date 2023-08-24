from rest_framework import serializers
from . import models


class Tag(serializers.ModelSerializer):

    class Meta:
        model = models.Tag
        fields = '__all__'


class Post(serializers.ModelSerializer):
    tags = Tag(many=True, required=False)

    class Meta:
        model = models.Post
        exclude = ('user',)

    def create(self, validated_data):
        user = self.context['request'].user
        user_profile = models.UserProfile.objects.filter(user=user).first()
        validated_data['user'] = user_profile
        return super().create(validated_data)


class UserProfile(serializers.ModelSerializer):
    post = Post

    class Meta:
        model = models.UserProfile
        exclude = ('user',)
