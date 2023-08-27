from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from core.filters import TagFilters
from core.models import PostModel, TagModel
from core.serializers import PostSerializer, TagSerializer


class TagViewSet(ModelViewSet):
    queryset = TagModel.objects.all()
    serializer_class = TagSerializer
    authentication_classes = (SessionAuthentication,)
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = TagFilters


class PostViewSet(ModelViewSet):
    queryset = PostModel.objects.all()
    serializer_class = PostSerializer
    authentication_classes = (SessionAuthentication,)
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.validated_data["user"] = self.request.user
        serializer.save()
