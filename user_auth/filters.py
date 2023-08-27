import django_filters

from user_auth.models import UserModel


class UserFilter(django_filters.FilterSet):
    username = django_filters.CharFilter(field_name="username", lookup_expr="icontains")

    class Meta:
        model = UserModel
        fields = ("username",)
