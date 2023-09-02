from core.models import LikeModel
from django.contrib.contenttypes.models import ContentType

from user_auth.models import UserModel


def add_like(obj, user):
    """
    Лайкает `obj`.
    """
    obj_type = ContentType.objects.get_for_model(obj)
    like, is_created = LikeModel.objects.get_or_create(
        content_type=obj_type, object_id=obj.id, user=user)
    return like


def remove_like(obj, user):
    """
    Удаляет лайк с `obj`.
    """
    obj_type = ContentType.objects.get_for_model(obj)
    LikeModel.objects.filter(
        content_type=obj_type, object_id=obj.id, user=user
    ).delete()


def is_fan(obj, user) -> bool:
    """
    Проверяет, лайкнул ли `user` `obj`.
    """
    if not user.is_authenticated:
        return False
    obj_type = ContentType.objects.get_for_model(obj)
    likes = LikeModel.objects.filter(
        content_type=obj_type, object_id=obj.id, user=user)
    return likes.exists()


def get_fans(obj):
    """
    Получает всех пользователей, которые лайкнули `obj`.
    """
    obj_type = ContentType.objects.get_for_model(obj)
    return UserModel.objects.filter(
        likes__content_type=obj_type, likes__object_id=obj.id)

