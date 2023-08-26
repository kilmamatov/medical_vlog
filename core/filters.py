import django_filters

from core.models import TagModel


class TagFilters(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name="name", lookup_expr="icontains")

    class Meta:
        model = TagModel
        fields = ("name",)


class PostFilters(django_filters.FilterSet):
    user = django_filters.CharFilter(field_name="user", lookup_expr="icontains")
    title = django_filters.CharFilter(field_name="title", lookup_expr="icontains")
    text = django_filters.CharFilter(field_name="text", lookup_expr="icontains")
    TagModels = django_filters.CharFilter(
        field_name="TagModels", lookup_expr="icontains"
    )

    class Meta:
        model = TagModel
        exclude = ("id",)
