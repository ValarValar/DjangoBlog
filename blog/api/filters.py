from django.db.models import Count
from rest_framework.filters import OrderingFilter


class CustomOrderingFilter(OrderingFilter):
    def filter_queryset(self, request, queryset, view):
        ordering = self.get_ordering(request, queryset, view)

        #if ordering:
            #if 'posts__count' in ordering or '-posts__count' in ordering:
                #queryset = queryset.annotate(Count('posts'))
        if ordering:
            return queryset.order_by(*ordering)

        return queryset
