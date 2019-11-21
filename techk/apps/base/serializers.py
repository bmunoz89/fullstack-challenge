# -*- coding: utf-8 -*-
from rest_framework import serializers

from .models import Book, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', )


class BookSerializer(serializers.ModelSerializer):
    price = serializers.DecimalField(max_digits=9, decimal_places=2, coerce_to_string=False)
    category = CategorySerializer()

    class Meta:
        model = Book
        fields = (
            'id',
            'title',
            'thumbnail_url',
            'price',
            'stock',
            'product_description',
            'upc',
            'category', )
