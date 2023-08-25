from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

urlpatterns = [

]

router = DefaultRouter()
router.register('tags', views.TagViewSet, basename='tags')
router.register('post', views.PostViewSet, basename='post')
router.register('user_profiles', views.UserProfileViewSet, basename='user_profiles')
urlpatterns += router.urls
