import sys
from collections import OrderedDict
from functools import cached_property

from django.core.paginator import Paginator
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPaginatorClass(Paginator):
    """
        Переопределяем аттрибут,чтобы не вызывать для каждой страницы пагинации count в бд
    """
    @cached_property
    def count(self):
        return sys.maxsize


class CustomPageNumberPagination(PageNumberPagination):
    """
        Мы написали свой пагинатор, который не вызывает для каждой страницы пагинации
        count query
    """
    django_paginator_class = CustomPaginatorClass
    page_size = 10

    def get_paginated_response(self, data):
        """
            Переопределяем, так как в count у нас теперь неправильное количество
            да и необходимости в нем нет.
        :param data:
        :return:
        """
        return Response(OrderedDict([
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data)
        ]))
