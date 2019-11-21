from django.test import SimpleTestCase

from apps.base.models import Book, Category
from apps.base.serializers import BookSerializer, CategorySerializer


class BookSerializerTestCase(SimpleTestCase):

    def test_expected_serialized_json(self):
        expected_results = {
            'id': 1,
            'title': 'Short title',
            'thumbnail_url': 'http://test.x/thumbnail.jpg',
            'price': 40.59,
            'stock': False,
            'product_description': 'Long description',
            'upc': 'qwertyuiopasdfgh',
            'category': None,
        }

        book = Book(**expected_results)

        results = BookSerializer(book).data
        results['price'] = float(results['price'])

        self.assertDictEqual(results, expected_results)

    def test_missing_required_fields(self):
        incomplete_data = {}

        serializer = BookSerializer(data=incomplete_data)

        serializer.is_valid(raise_exception=False)
        self.assertDictEqual(serializer.errors, {
            'category': ['This field is required.'],
            'price': ['This field is required.'],
            'product_description': ['This field is required.'],
            'thumbnail_url': ['This field is required.'],
            'title': ['This field is required.'],
            'upc': ['This field is required.'],
        })


class CategorySerializerTestCase(SimpleTestCase):

    def test_expected_serialized_json(self):
        expected_results = {
            'id': 1,
            'name': 'Travel',
        }

        category = Category(**expected_results)

        results = CategorySerializer(category).data

        self.assertDictEqual(results, expected_results)

    def test_missing_required_fields(self):
        incomplete_data = {}

        serializer = CategorySerializer(data=incomplete_data)

        serializer.is_valid(raise_exception=False)
        self.assertDictEqual(serializer.errors, {
            'name': ['This field is required.'],
        })
