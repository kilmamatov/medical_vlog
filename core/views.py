from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from core.models import Tag, Post
from user_auth.models import UserModel
from core.serializers import TagSerializer, PostSerializer
from user_auth.serializers import UserSerializer

class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    # def post(self, request):


class UserProfileViewSet(ModelViewSet):
    """
    Добавить проверку есть ли уже юзер профиль и не создавать его в случае чего
    """
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        serializer.validated_data['user'] = self.request.user
        serializer.save()


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.validated_data['user'] = self.request.user
        serializer.save()

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
