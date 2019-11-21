# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django_filters import rest_framework as filters
from rest_framework import mixins, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.viewsets import GenericViewSet

from .filters import BookFilter
from .models import Book, Category
from .serializers import BookSerializer, CategorySerializer


class BookView(mixins.ListModelMixin, mixins.DestroyModelMixin, GenericViewSet):
    queryset = Book.objects.select_related('category').all()
    serializer_class = BookSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.DjangoFilterBackend, )
    filterset_class = BookFilter


class CategoryView(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
