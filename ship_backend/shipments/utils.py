import operator
from functools import reduce

from django.contrib.auth.models import User
from django.db.models import QuerySet, Q
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import Field
from rest_framework import pagination
from rest_framework.response import Response


class CustomPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'page_size': self.get_page_size(self.request),
            'page_number': int(self.request.query_params.get(self.page_query_param, 1)),
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data
        })


class OptionsMappingField(Field):
    def __init__(self, options, **kwargs):
        self.options = dict(options)
        self.reversed_options = dict((value, key) for key, value in options)

        super(OptionsMappingField, self).__init__(**kwargs)

    def to_representation(self, obj):
        return self.options.get(obj)

    def to_internal_value(self, data):
        value = self.reversed_options.get(data)
        if value is None:
            raise ValidationError('Not valid option.')

        return value


class SimpleTextSearchMixin:
    search_fields = NotImplementedError

    @staticmethod
    def _search_fields_to_substring(search_fields):
        return [f + '__contains' for f in search_fields]

    def convert_search_to_simple_search(self, queryset, search_fields) -> QuerySet:
        substring_search_fields = self._search_fields_to_substring(search_fields)
        return self._simple_search(queryset, substring_search_fields)

    def _simple_search(self, queryset, substring_search_fields):
        search_term = self.request.query_params.get('simple_search')
        if search_term:
            predicates = [(field_name, search_term) for field_name in substring_search_fields]

            q_list = [Q(x) for x in predicates]
            filter_clause = reduce(operator.or_, q_list)

            queryset = queryset.filter(filter_clause)

        return queryset
