from django.urls import path, include

from user_auth.views import RegisterUserView

auth = [
    path("create_user/", RegisterUserView.as_view()),
]

urlpatterns = [
    path("registration/", include(auth)),
]
