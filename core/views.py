from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from . import models
from . import serializers


class TagViewSet(ModelViewSet):
    queryset = models.Tag.objects.all()
    serializer_class = serializers.Tag


class UserProfileViewSet(ModelViewSet):
    """
    добавить проверку есть ли уже узер профиль и не создавать его в случае чего
    """
    queryset = models.UserProfile.objects.all()
    serializer_class = serializers.UserProfile

    def perform_create(self, serializer):
        serializer.validated_data['user'] = self.request.user
        serializer.save()


# class PostViewSet(ModelViewSet):
#     queryset = models.Post.objects.all()
#     serializer_class = serializers.Post
#
#     def perform_create(self, serializer):
#         serializer.validated_data['user'] = self.request.user
#         serializer.save()


