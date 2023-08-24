from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.response import Response
from . import models, filters
from . import serializers


class TagViewSet(ModelViewSet):
    queryset = models.Tag.objects.all()
    serializer_class = serializers.Tag
    filter_backends = [DjangoFilterBackend]
    filterset_class = filters.Tag


class UserProfileViewSet(ModelViewSet):
    """
    добавить проверку есть ли уже узер профиль и не создавать его в случае чего
    """
    queryset = models.UserProfile.objects.all()
    serializer_class = serializers.UserProfile
    filter_backends = [DjangoFilterBackend]
    filterset_class = filters.UserProfile

    def perform_create(self, serializer):
        serializer.validated_data['user'] = self.request.user
        serializer.save()


class PostViewSet(ModelViewSet):
    queryset = models.Post.objects.all()
    serializer_class = serializers.Post

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


