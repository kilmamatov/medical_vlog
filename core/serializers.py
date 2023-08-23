from rest_framework import serializers
from . import models


class Tag(serializers.ModelSerializer):

    class Meta:
        model = models.Tag
        fields = '__all__'


class Post(serializers.ModelSerializer):
    tags = Tag(many=True)

    class Meta:
        model = models.Post
        exclude = ('user',)


class UserProfile(serializers.ModelSerializer):
    post = Post

    class Meta:
        model = models.UserProfile
        exclude = ('user',)
