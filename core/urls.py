from django.urls import path
from rest_framework.routers import DefaultRouter

from core.views import CommentViewSet, PostViewSet, TagViewSet, NewsAPIView

urlpatterns = [
    path('news-api/', NewsAPIView.as_view(), name='news-api')
]

router = DefaultRouter()
router.register("tags", TagViewSet, basename="tag")
router.register("posts", PostViewSet, basename="post")
router.register(r"posts/(?P<slug>[-\w]+)/comments", CommentViewSet, basename="comment")

urlpatterns += router.urls
