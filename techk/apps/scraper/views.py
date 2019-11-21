# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.base.models import Book, Category

from .providers import BooksToScrape


class ScraperView(APIView):

    def _update_categories(self):
        categories_name = self.books_to_scrape.get_categories()

        total_inserted = 0
        total_deleted = 0
        if len(categories_name):
            total_deleted, _ = Category.objects.exclude(name__in=categories_name).delete()

            all_categories = Category.objects.all()
            categories_by_name = {
                category.name: category
                for category in all_categories
            }

            bulk_categories = []
            for category_name in categories_name:
                if category_name not in categories_by_name:
                    category_model = Category(name=category_name)
                    categories_by_name[category_name] = category_model
                    bulk_categories.append(category_model)
                    total_inserted += 1

            if len(bulk_categories):
                Category.objects.bulk_create(bulk_categories)
        return {
            'inserted': total_inserted,
            'updated': 0,
            'deleted': total_deleted,
        }

    def _update_books(self):
        all_books = Book.objects.only('id', 'last_modified').all()
        last_modified_book_by_id = {
            book.id: book.last_modified
            for book in all_books
        }

        all_categories = Category.objects.all()
        categories_by_name = {
            category.name: category
            for category in all_categories
        }

        bulk_books = []
        books_id = []
        total_updated = 0
        total_inserted = 0
        for basic_book_data in self.books_to_scrape.get_all():
            book_id = basic_book_data['id']
            update = False
            last_modified = None
            if book_id in last_modified_book_by_id:
                last_modified = last_modified_book_by_id[book_id]
                update = True

            books_id.append(book_id)

            book_data = self.books_to_scrape.get_detail(
                basic_book_data['url'], last_modified)

            if book_data is None:
                continue

            category = categories_by_name[book_data['category']]
            price = float(book_data['price'].replace('£', ''))
            book_model_data = {
                'title': book_data['title'],
                'thumbnail_url': book_data['thumbnail_url'],
                'price': price,
                'stock': book_data['stock'],
                'product_description': book_data['product_description'],
                'upc': book_data['upc'],
                'last_modified': book_data['last_modified'],
                'category': category,
            }
            if update is True:
                Book.objects.filter(id=book_id).update(**book_model_data)
                total_updated += 1
            else:
                book_model_data['id'] = book_id
                book_model = Book(**book_model_data)
                bulk_books.append(book_model)
                total_inserted += 1

        if len(bulk_books):
            Book.objects.bulk_create(bulk_books)

        total_deleted, _ = Book.objects.exclude(id__in=books_id).delete()
        return {
            'inserted': total_inserted,
            'updated': total_updated,
            'deleted': total_deleted,
        }

    def post(self, request):
        try:
            self.books_to_scrape = BooksToScrape()
            categories_stats = self._update_categories()
            books_stats = self._update_books()
        except Exception:
            return Response({
                'status': 'Error',
                'detail': 'Unexpected error',
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({
            'status': 'ok',
            'categories_stats': categories_stats,
            'books_stats': books_stats,
        })
