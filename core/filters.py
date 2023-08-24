import django_filters
from . import models


class Tag(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = models.Tag
        exclude = ('id',)


class UserProfile(django_filters.FilterSet):
    nickname = django_filters.CharFilter(field_name='nickname', lookup_expr='icontains')

    class Meta:
        model = models.Tag
        exclude = ('id', 'user', 'photo', 'description')

