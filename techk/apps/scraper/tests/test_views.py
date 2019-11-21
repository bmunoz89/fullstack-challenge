# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import re

import requests_mock
from django.conf import settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase, URLPatternsTestCase

import config.urls

requests_mock.Mocker.TEST_PREFIX = 'test_'


@requests_mock.mock()
class ScraperViewTests(APITestCase, URLPatternsTestCase):
    urlpatterns = config.urls.urlpatterns
    URLs = {
        'main': 'http://books.toscrape.com/',
        'book-first-page': 'http://books.toscrape.com/catalogue/page-1.html',
        'book-last-page': 'http://books.toscrape.com/catalogue/page-2.html',
        'book-detail': re.compile(r'http://books\.toscrape\.com/catalogue/.*/index\.html'),
    }
    last_modified = 'Wed, 29 Jun 2016 21:15:59 GMT'

    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()

    def _mock_urls(self, mock):
        for html_name, url in self.URLs.items():
            file_path = os.path.join(
                settings.BASE_DIR,
                f'apps/scraper/tests/responses/{html_name}.html')

            with open(file_path, mode='rb') as file:
                mock.register_uri(
                    'GET',
                    url,
                    headers={
                        'Last-Modified': self.last_modified,
                    },
                    content=file.read(),
                    status_code=status.HTTP_200_OK)

    def test_update(self, mock):
        self._mock_urls(mock)

        url = reverse('scraper')
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(response.json(), {
            'status': 'ok',
            'books_stats': {'deleted': 9, 'inserted': 34, 'updated': 6},
            'categories_stats': {'deleted': 0, 'inserted': 47, 'updated': 0},
        })
