from rest_framework.decorators import action
from rest_framework.response import Response

from core import services


class PostLikedMixin:
    @action(methods=['POST'], detail=True)
    def like_post(self, request, slug=None):
        obj = self.get_object()
        services.add_like(obj, request.user)
        return Response()

    @action(methods=['POST'], detail=True)
    def unlike_post(self, request, slug=None):
        obj = self.get_object()
        services.remove_like(obj, request.user)
        return Response()


class CommentLikedMixin:
    @action(methods=['POST'], detail=True)
    def like_comment(self, request, slug=None, pk=None):
        obj = self.get_object()
        services.add_like(obj, request.user)
        return Response()

    @action(methods=['POST'], detail=True)
    def unlike_comment(self, request, slug=None, pk=None):
        obj = self.get_object()
        services.remove_like(obj, request.user)
        return Response()
