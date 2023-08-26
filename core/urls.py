from rest_framework.routers import DefaultRouter

from core.views import PostViewSet, TagViewSet, UserProfileViewSet

urlpatterns = []

router = DefaultRouter()
router.register("tags", TagViewSet, basename="tags")
router.register("user_profiles", UserProfileViewSet, basename="user_profiles")
router.register("posts", PostViewSet, basename="posts")
urlpatterns += router.urls
