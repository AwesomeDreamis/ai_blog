from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from django_filters import rest_framework as filters
from app_news_board.models import News, Images, Comment
from app_users.models import Profile
from django.contrib.auth.models import User
from django.db.models import Q


# class BooksFilter(filters.FilterSet):
#     """Пользовательский поиск по диапазону года выпуска книг"""
#
#     year = filters.RangeFilter()
#
#     class Meta:
#         model = Book
#         fields = ['year', ]


class CustomPagination(PageNumberPagination):
    """Пользовательская пагинация"""
    page_size = 3

    def get_paginated_response(self, data):
        """
        Каким образом выводится информация о пагинации
        :param data: Выводящиеся объекты
        :return: Информация о пагинации
        """
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link(),
            },
            'count': self.page.paginator.count,
            'result': data,
        })
