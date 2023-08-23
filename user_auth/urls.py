from django.urls import path, include
from . import views


auth = [
    path('create_user/', views.RegisterUser.as_view()),
    path('login_user/', views.LoginUser.as_view()),
]

urlpatterns = [
    path('registration/', include(auth)),
]
