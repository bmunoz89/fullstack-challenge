from email.utils import parsedate_to_datetime

import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from rest_framework import status


def requests_retry_session(
    retries=3,
    backoff_factor=0.3,
    status_forcelist=(
        status.HTTP_500_INTERNAL_SERVER_ERROR,
        status.HTTP_502_BAD_GATEWAY,
        status.HTTP_504_GATEWAY_TIMEOUT
    ),
):
    """Return an HTTP session that tries 3 times before throw an exception."""
    session = requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session


class BooksToScrape:
    timeout = 2
    main_url = 'http://books.toscrape.com/'
    catalog_url = main_url + 'catalogue/'
    soup = None

    def __init__(self):
        self._session = requests_retry_session()

    def get_categories(self):
        response = self._session.get(self.main_url, timeout=self.timeout)
        response.raise_for_status()

        self.soup = BeautifulSoup(response.content, 'html.parser')

        categories = []
        category_elements = self.soup.select('.side_categories ul li ul li a')
        for category_element in category_elements:
            category = category_element\
                .get_text()\
                .strip()
            categories.append(category)
        return categories

    def get_detail(self, url, last_modified=None):
        last_modified_header = None
        if last_modified is not None:
            response = self._session.head(url, timeout=self.timeout)

            last_modified_header = parsedate_to_datetime(response.headers['Last-Modified'])

            if last_modified >= last_modified_header:
                return None

        response = self._session.get(url, timeout=self.timeout)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        book = {}
        # Get last modified
        if last_modified_header is None:
            book['last_modified'] = parsedate_to_datetime(response.headers['Last-Modified'])
        else:
            book['last_modified'] = last_modified_header
        # Get category
        book['category'] = soup.select_one('ul.breadcrumb li:nth-of-type(3)')\
            .get_text()\
            .strip()

        product_page = soup.select_one('.product_page')
        # Get title
        book['title'] = product_page.select_one('.product_main h1')\
            .get_text()\
            .strip()
        # Get thumbnail
        thumbnail_src = product_page.select_one('#product_gallery img')\
            .attrs['src']\
            .replace('../../', '')
        book['thumbnail_url'] = self.main_url + thumbnail_src
        # Get price
        book['price'] = product_page.select_one('.price_color')\
            .get_text()\
            .strip()

        # Get product description
        product_description = product_page.select_one('#product_description')
        book['product_description'] = ''
        if product_description is not None:
            book['product_description'] = product_description\
                .next_sibling\
                .next_sibling\
                .get_text()\
                .replace('...more', '')\
                .strip()

        product_table = product_page.select_one('table')
        # Get stock
        book['stock'] = product_table.select_one('tr:nth-of-type(6) td')\
            .get_text() != 'In stock (0 available)'
        # Get UPC
        book['upc'] = product_table.select_one('tr:nth-of-type(1) td')\
            .get_text()

        return book

    def get_all(self):
        page_number = 1
        while True:
            url = f'{self.catalog_url}page-{page_number}.html'
            response = self._session.get(url, timeout=self.timeout)
            response.raise_for_status()

            self.soup = BeautifulSoup(response.content, 'html.parser')
            book_elements = self.soup.select('section article.product_pod h3 a')
            for book_element in book_elements:
                book_url = self.catalog_url + book_element.attrs['href']
                try:
                    book_id = int(book_url.split('/')[-2].split('_')[1])
                except Exception as exc:
                    raise Exception('Unable to get id') from exc

                yield {
                    'id': book_id,
                    'url': book_url,
                }

            next_link = self.soup.select_one('.pager .next a')
            if next_link is None:
                break
            page_number += 1
