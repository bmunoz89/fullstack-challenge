# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
from datetime import timedelta
from email.utils import parsedate_to_datetime

import requests_mock
from django.conf import settings
from django.test import TestCase
from rest_framework import status

from ..providers import BooksToScrape

requests_mock.Mocker.TEST_PREFIX = 'test_'


@requests_mock.mock()
class BooksToScrapeTests(TestCase):
    URLs = {
        'main': 'http://books.toscrape.com/',
        'first_page': 'http://books.toscrape.com/catalogue/page-1.html',
        'last_page': 'http://books.toscrape.com/catalogue/page-2.html',
        'detail': 'http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html',
        'detail_without_description': (
            'http://books.toscrape.com/catalogue/the-bridge-to-consciousness-im-writing-the-bridge'
            '-between-science-and-our-old-and-new-beliefs_840/index.html'),
    }
    categories = [
        'Travel', 'Mystery', 'Historical Fiction', 'Sequential Art', 'Classics', 'Philosophy',
        'Romance', 'Womens Fiction', 'Fiction', 'Childrens', 'Religion', 'Nonfiction', 'Music',
        'Default', 'Science Fiction', 'Sports and Games', 'Add a comment', 'Fantasy', 'New Adult',
        'Young Adult', 'Science', 'Poetry', 'Paranormal', 'Art', 'Psychology', 'Autobiography',
        'Parenting', 'Adult Fiction', 'Humor', 'Horror', 'History', 'Food and Drink',
        'Christian Fiction', 'Business', 'Biography', 'Thriller', 'Contemporary', 'Spirituality',
        'Academic', 'Self Help', 'Historical', 'Christian', 'Suspense', 'Short Stories', 'Novels',
        'Health', 'Politics', 'Cultural', 'Erotica', 'Crime'
    ]
    last_modified = 'Wed, 29 Jun 2016 21:15:59 GMT'

    def test_categories(self, mock):
        file_path = os.path.join(
            settings.BASE_DIR,
            'apps/scraper/tests/responses/main.html')

        url = self.URLs['main']
        with open(file_path, mode='rb') as file:
            mock.register_uri(
                'GET',
                url,
                headers={
                    'Last-Modified': self.last_modified,
                },
                content=file.read(),
                status_code=status.HTTP_200_OK)

        books_to_scrape = BooksToScrape()
        categories = books_to_scrape.get_categories()
        self.assertListEqual(
            categories, self.categories)

    def test_books(self, mock):
        file_path = os.path.join(
            settings.BASE_DIR,
            'apps/scraper/tests/responses/book-first-page.html')

        url = self.URLs['first_page']
        with open(file_path, mode='rb') as file:
            mock.register_uri(
                'GET',
                url,
                headers={
                    'Last-Modified': self.last_modified,
                },
                content=file.read(),
                status_code=status.HTTP_200_OK)

        file_path = os.path.join(
            settings.BASE_DIR,
            'apps/scraper/tests/responses/book-last-page.html')

        url = self.URLs['last_page']
        with open(file_path, mode='rb') as file:
            mock.register_uri(
                'GET',
                url,
                headers={
                    'Last-Modified': self.last_modified,
                },
                content=file.read(),
                status_code=status.HTTP_200_OK)

        books_to_scrape = BooksToScrape()
        count_elements = 0
        for book in books_to_scrape.get_all():
            self.assertIsInstance(book, dict)
            book_keys = list(book.keys())
            self.assertListEqual(book_keys, [
                'id',
                'url',
            ])
            self.assertIsInstance(book['id'], int)
            self.assertIsInstance(book['url'], str)
            self.assertNotEqual(book['url'], '')
            count_elements += 1
        self.assertEqual(count_elements, 40, 'Quantity of books must be 40')

    def test_book_detail(self, mock):
        file_path = os.path.join(
            settings.BASE_DIR,
            'apps/scraper/tests/responses/book-detail.html')

        url = self.URLs['detail']
        with open(file_path, mode='rb') as file:
            mock.register_uri(
                'GET',
                url,
                headers={
                    'Last-Modified': self.last_modified,
                },
                content=file.read(),
                status_code=status.HTTP_200_OK)

        mock.register_uri(
            'HEAD',
            url,
            headers={
                'Last-Modified': self.last_modified,
            },
            status_code=status.HTTP_200_OK)

        books_to_scrape = BooksToScrape()
        last_modified = parsedate_to_datetime(self.last_modified) - timedelta(seconds=1)
        book_detail = books_to_scrape.get_detail(url, last_modified=last_modified)
        self.assertIsInstance(book_detail, dict)
        book_keys = list(book_detail.keys())
        self.assertListEqual(book_keys, [
            'last_modified',
            'category',
            'title',
            'thumbnail_url',
            'price',
            'product_description',
            'stock',
            'upc',
        ])
        self.assertIn(book_detail['category'], self.categories)
        self.assertEqual(book_detail['title'], 'A Light in the Attic')
        self.assertEqual(
            book_detail['thumbnail_url'],
            'http://books.toscrape.com/media/cache/fe/72/fe72f0532301ec28892ae79a629a293c.jpg')
        self.assertEqual(book_detail['price'], '£51.77')
        self.assertEqual(book_detail['product_description'], (
            "It's hard to imagine a world without A Light in the Attic. This now-classic"
            " collection of poetry and drawings from Shel Silverstein celebrates its 20th"
            " anniversary with this special edition. Silverstein's humorous and creative verse"
            " can amuse the dowdiest of readers. Lemon-faced adults and fidgety kids sit still"
            " and read these rhythmic words and laugh and smile and love th It's hard to"
            " imagine a world without A Light in the Attic. This now-classic collection of"
            " poetry and drawings from Shel Silverstein celebrates its 20th anniversary with"
            " this special edition. Silverstein's humorous and creative verse can amuse the"
            " dowdiest of readers. Lemon-faced adults and fidgety kids sit still and read"
            " these rhythmic words and laugh and smile and love that Silverstein. Need proof"
            " of his genius? RockabyeRockabye baby, in the treetopDon't you know a treetopIs"
            " no safe place to rock?And who put you up there,And your cradle, too?Baby, I"
            " think someone down here'sGot it in for you. Shel, you never sounded so good."))
        self.assertTrue(book_detail['stock'])
        self.assertEqual(book_detail['upc'], 'a897fe39b1053632')

    def test_book_detail_not_modified(self, mock):
        url = self.URLs['detail']
        mock.register_uri(
            'HEAD',
            url,
            headers={
                'Last-Modified': self.last_modified,
            },
            status_code=status.HTTP_200_OK)

        last_modified = parsedate_to_datetime(self.last_modified)
        books_to_scrape = BooksToScrape()
        book_detail = books_to_scrape.get_detail(url, last_modified=last_modified)
        self.assertIsNone(book_detail)

    def test_book_detail_without_product_description(self, mock):
        file_path = os.path.join(
            settings.BASE_DIR,
            'apps/scraper/tests/responses/book-detail-without-description.html')

        url = self.URLs['detail_without_description']
        with open(file_path, mode='rb') as file:
            mock.register_uri(
                'GET',
                url,
                headers={
                    'Last-Modified': self.last_modified,
                },
                content=file.read(),
                status_code=status.HTTP_200_OK)

        books_to_scrape = BooksToScrape()
        book_detail = books_to_scrape.get_detail(url)
        self.assertIsInstance(book_detail, dict)
        book_keys = list(book_detail.keys())
        self.assertListEqual(book_keys, [
            'last_modified',
            'category',
            'title',
            'thumbnail_url',
            'price',
            'product_description',
            'stock',
            'upc',
        ])
        self.assertEqual(book_detail['product_description'], '')
