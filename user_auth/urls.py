from django.urls import include, path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from user_auth.views import RegisterUserView, UserProfileView

auth = [
    path("create_user/", RegisterUserView.as_view()),
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token-refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]

urlpatterns = [
    path("auth/", include(auth)),
    path("profile/", UserProfileView.as_view(), name="profile"),
]
