from django.contrib import admin
from django.urls import include, path
from rest_framework_swagger.views import get_swagger_view

from core import urls as urls_core
from user_auth import urls as urls_user

schema_view = get_swagger_view(title="API")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include(urls_core)),
    path("user/", include(urls_user)),
    path("", schema_view),
]
