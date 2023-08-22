from django.contrib import admin
from django.urls import path, include
from core import urls as urls_core
from user_auth import urls as urls_user

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(urls_core)),
    path('user/', include(urls_user)),
]
