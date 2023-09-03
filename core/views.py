import os

import requests
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from core.filters import TagFilters
from core.mixins import CommentLikedMixin
from core.models import CommentModel, PostModel, TagModel
from core.serializers import CommentSerializer, PostSerializer, TagSerializer
from core.utils import manage_items_to_redis_save


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
    # authentication_classes = (SessionAuthentication,)
    permission_classes = [IsAuthenticated]
    lookup_field = "slug"


class CommentViewSet(CommentLikedMixin, ModelViewSet):
    queryset = CommentModel.objects.all()
    serializer_class = CommentSerializer
    authentication_classes = (SessionAuthentication,)
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        post_slug = self.kwargs["slug"]
        post = PostModel.objects.get(slug=post_slug)
        serializer.save(user=self.request.user, post=post)


class NewsAPIView(APIView):
    def get(self, request):
        url = "https://newsapi.org/v2/top-headlines"
        params = {
            "country": "ru",
            "apiKey": os.getenv("NEWS_API_KEY"),
        }
        response = requests.get(url, params=params)
        data = response.json()
        manage_items_to_redis_save("articles", data)
        return Response(data)
