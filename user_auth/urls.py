from django.urls import include, path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from user_auth.views import RegisterUserView, UserProfileView, LoginUserView

auth = [
    path("create_user/", RegisterUserView.as_view()),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token-refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("profile/", UserProfileView.as_view(), name="profile"),
    path("login/", LoginUserView.as_view(), name="login"),
]

urlpatterns = [
    path("auth/", include(auth)),
]
