from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from core.filters import TagFilters
from core.models import PostModel, TagModel
from core.serializers import PostSerializer, TagSerializer, UserProfile
from user_auth.filters import UserFilter
from user_auth.models import UserModel


class TagViewSet(ModelViewSet):
    queryset = TagModel.objects.all()
    serializer_class = TagSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = TagFilters


# class UserProfileViewSet(ModelViewSet):
#     queryset = UserModel.objects.all()
#     serializer_class = UserProfile
#     filter_backends = [DjangoFilterBackend]
#     filterset_class = UserFilter
#
#     def perform_create(self, serializer):
#         serializer.validated_data["user"] = self.request.user
#         serializer.save()


class PostViewSet(ModelViewSet):
    queryset = PostModel.objects.all()
    serializer_class = PostSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
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
