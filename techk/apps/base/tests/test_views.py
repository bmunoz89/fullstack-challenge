# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase, URLPatternsTestCase

import config.urls
from apps.base.models import Book, Category
from apps.base.serializers import BookSerializer, CategorySerializer


class BookViewTests(APITestCase, URLPatternsTestCase):
    urlpatterns = config.urls.urlpatterns

    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()

    def test_list(self):
        url = reverse('book-list')
        with self.assertNumQueries(2):
            response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        books_queryset = Book.objects.select_related('category').all()
        serializer = BookSerializer(books_queryset, many=True)

        response_json = response.json()
        self.assertIn('results', response_json)
        self.assertEqual(len(response_json['results']), 15)

        for index, result in enumerate(response_json['results']):
            result_keys = list(result.keys())
            self.assertListEqual(result_keys, [
                'id',
                'title',
                'thumbnail_url',
                'price',
                'stock',
                'product_description',
                'upc',
                'category',
            ])

            serializer_data = serializer.data[index]
            serializer_data['price'] = float(serializer_data['price'])

            self.assertDictEqual(result, serializer_data)

    def test_delete(self):
        book_id = 981
        url = reverse('book-detail', kwargs={'pk': book_id})
        with self.assertNumQueries(2):
            response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        with self.assertRaises(Book.DoesNotExist):
            Book.objects.get(id=book_id)


class CategoryViewTests(APITestCase, URLPatternsTestCase):
    urlpatterns = config.urls.urlpatterns

    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()

    def test_list(self):
        url = reverse('category-list')
        with self.assertNumQueries(1):
            response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        categories_queryset = Category.objects.all()
        serializer = CategorySerializer(categories_queryset, many=True)

        response_json = response.json()
        self.assertEqual(len(response_json), 3)

        for index, result in enumerate(response_json):
            result_keys = list(result.keys())
            self.assertListEqual(result_keys, [
                'id',
                'name',
            ])

            serializer_data = serializer.data[index]
            self.assertDictEqual(result, serializer_data)
