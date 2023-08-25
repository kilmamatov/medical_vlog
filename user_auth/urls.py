from django.urls import path, include
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

auth = [
    path('create_user/', views.RegisterUser.as_view()),
    path('login_user/', views.LoginUser.as_view()),
]

urlpatterns = [
    path('registration/', include(auth)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
