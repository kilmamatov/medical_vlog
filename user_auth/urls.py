from django.urls import include, path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from user_auth.views import (
    LogoutUserView,
    MyTokenObtainPairView,
    RegisterUserView,
    UserModelView,
    VerifyEmail,
)

app_name = "user_auth"

auth = [
    path("create_user/", RegisterUserView.as_view(), name="registration"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token-refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("login/", MyTokenObtainPairView.as_view(), name="login"),
    path("logout/", LogoutUserView.as_view(), name="logout"),
    path("email-verify/", VerifyEmail.as_view(), name="email-verify"),
]

urlpatterns = [
    path("auth/", include(auth)),
    path("profile/<int:pk>", UserModelView.as_view(), name="profile"),
]
