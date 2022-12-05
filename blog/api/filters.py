from django_filters import rest_framework as filters

from .models import Post


class PostSeenFilter(filters.FilterSet):
    """
        Filterset which allows to filter by non-model field - seen.
        Users manually mark post as seen, so filterset allows to filter by value of this mark.
    """
    seen = filters.BooleanFilter(field_name='seen', method='filter_seen')

    class Meta:
        model = Post
        fields = ['seen']

    def filter_seen(self, queryset, name, value):
        return queryset.filter(**{name: value})
