from rest_framework.routers import DefaultRouter

from core.views import PostViewSet, TagViewSet, CommentViewSet

urlpatterns = []

router = DefaultRouter()
router.register("tags", TagViewSet, basename="tag")
router.register("posts", PostViewSet, basename="post")
router.register(r'posts/(?P<slug>[-\w]+)/comments', CommentViewSet, basename='comment')
urlpatterns += router.urls
