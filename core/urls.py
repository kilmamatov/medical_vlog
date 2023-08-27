from rest_framework.routers import DefaultRouter

from core.views import PostViewSet, TagViewSet

urlpatterns = []

router = DefaultRouter()
router.register("tags", TagViewSet, basename="tags")
router.register("posts", PostViewSet, basename="posts")
urlpatterns += router.urls
