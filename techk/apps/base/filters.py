# -*- coding: utf-8 -*-
from django_filters import rest_framework as filters

from .models import Book, Category


class BookFilter(filters.FilterSet):
    title = filters.CharFilter(lookup_expr='icontains')
    product_description = filters.CharFilter(lookup_expr='icontains')
    stock = filters.BooleanFilter()
    price__gt = filters.NumberFilter(field_name='price', lookup_expr='gt')
    price__lt = filters.NumberFilter(field_name='price', lookup_expr='lt')
    category = filters.ModelMultipleChoiceFilter(
        field_name='category__name',
        to_field_name='name',
        queryset=Category.objects.all())

    class Meta:
        model = Book
        fields = (
            'title',
            'price',
            'stock',
            'product_description',
            'category', )
