import asyncio
import csv
import logging
import os
import re
import time
from pathlib import Path
from typing import List, Optional

import aiohttp
from aiohttp_retry import ExponentialRetry, RetryClient
from bs4 import BeautifulSoup

from api_books.services.scraper_exception import PaginatorNotFoundException, ScraperException
from api_books.settings import Settings

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    '(KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36 Edg/137.0.0.0'
}


class AsyncBookScraper:
    """Encapsula toda a lógica de scraping do site books.toscrape.com."""

    TARGET_URL = Settings().SCRAPING_TARGET_URL
    OUTPUT_CSV_FILE = Settings().CSV_PATH
    _current_id: int = 0

    def __init__(self, max_concurrent_requests: int = 15, logger: logging.Logger = None):
        self.max_concurrent_requests = max_concurrent_requests
        self.semaphore = asyncio.Semaphore(max_concurrent_requests)
        self.logger = logger
        self.session = None
        self.semaphore = None

        print(f'TARGET_URL configurada: {self.TARGET_URL}')
        if not self.TARGET_URL.endswith('/'):
            print('INFO: TARGET_URL não termina com /')

    async def _get_bs4(self, url: str) -> Optional[BeautifulSoup]:
        """Faz a requisição HTTP e retorna um objeto BeautifulSoup."""
        async with self.semaphore:
            try:
                async with self.session.get(url, timeout=5) as response:
                    response.raise_for_status()  # Lança HTTPError para status 4xx/5xx
                    html = await response.text()
                    return BeautifulSoup(html, 'html.parser')
            except (aiohttp.ClientError, asyncio.TimeoutError) as e:
                # self.logger.error(f"Erro ao acessar a URL: {url}", exc_info=True)
                print(f'Erro ao acessar {url}: {e}')
                print(f'Tipo do erro: {type(e)}')
                return None

    async def _get_total_pages(self) -> int:
        """Encontra e retorna o número total de páginas da paginação do site"""
        # self.logger.info("Buscando o número total de páginas...")
        bs4 = await self._get_bs4(self.TARGET_URL)

        if not bs4:
            raise ScraperException('Não foi possível abrir a página inicial.')

        paginator = bs4.find('li', class_='current')
        if not paginator:
            raise PaginatorNotFoundException(
                "Elemento de paginação 'li.current' não foi encontrado."
            )

        match = re.search(r'of (\d+)', paginator.text)

        total_pages = int(match.group(1))
        # self.logger.info(f"Total de páginas encontradas: {total_pages}")
        return total_pages

    @staticmethod
    def _get_book_title(book: BeautifulSoup) -> str:
        return book.h3.a['title']

    @staticmethod
    def _get_book_price(book: BeautifulSoup) -> float:
        price_text = book.find('p', class_='price_color').text
        pattern = r'\d+(\.\d+)?'
        match = re.search(pattern, price_text)
        return float(match.group(0))

    @staticmethod
    def _get_book_availability(book: BeautifulSoup) -> int:
        text = book.find('p', class_='instock availability').text.strip()
        match = re.search(r'\((\d+)\s+available\)', text)
        stock_qty = int(match.group(1)) if match else 0
        return stock_qty

    @staticmethod
    def _get_book_rating(book: BeautifulSoup) -> str:
        rating_text = book.find('p', class_='star-rating')['class'][1]
        word_to_num = {
            'zero': 0.0,
            'one': 1.0,
            'two': 2.0,
            'three': 3.0,
            'four': 4.0,
            'five': 5.0,
            'six': 6.0,
            'seven': 7.0,
            'eight': 8.0,
            'nine': 9.0,
            'ten': 10.0,
        }
        return word_to_num.get(rating_text.lower(), 0.0)

    def _get_image_url(self, book_detail: BeautifulSoup) -> str:
        image_src_value = book_detail.select_one('.carousel-inner img')['src']
        image_path = image_src_value.replace('../', '/')
        image_path = image_path.lstrip('/')
        base_url = self.TARGET_URL.rstrip('/') + '/'

        return base_url + image_path

    @staticmethod
    def _get_category(book_detail: BeautifulSoup) -> str:
        category = book_detail.select('ul.breadcrumb li a')[-1].text.strip()
        return category

    async def _access_page_detail(self, book_bs4: BeautifulSoup) -> BeautifulSoup:
        path_book_detail = book_bs4.h3.a['href'].replace('catalogue/', '')
        base_url = self.TARGET_URL.rstrip('/') + '/'
        url_book_detail = base_url + 'catalogue/' + path_book_detail
        book_detail_bs4 = await self._get_bs4(url_book_detail)
        if not book_detail_bs4:
            raise ScraperException('Não foi possível abrir a página de detalhes.')

        return book_detail_bs4

    async def _parse_book(self, book_bs4) -> Optional[List]:
        self._current_id += 1
        id = self._current_id
        title = self._get_book_title(book_bs4)
        price = self._get_book_price(book_bs4)
        # availability = self._get_book_availability(book_bs4)
        rating = self._get_book_rating(book_bs4)

        # image, category and availability
        # navegar até pagina de detalhes
        book_detail_bs4 = await self._access_page_detail(book_bs4)
        availability = self._get_book_availability(book_detail_bs4)
        category = self._get_category(book_detail_bs4)
        image_url = self._get_image_url(book_detail_bs4)

        return [id, title, price, availability, rating, category, image_url]

    def _generate_page_urls(self, total_pages: int) -> List[str]:
        """Gera lista de URLs para todas as páginas de paginação"""
        urls = []
        for page in range(1, total_pages + 1):
            # garantir que TARGET_URL termine com /
            base_url = self.TARGET_URL.rstrip('/') + '/'
            url = f'{base_url}catalogue/page-{page}.html'
            urls.append(url)
        return urls

    async def _fetch_all_pages(self, page_urls: List[str]) -> List[BeautifulSoup]:
        """Busca todas as páginas de forma assíncrona"""
        print(f'Buscando todas as {len(page_urls)} páginas...')
        page_tasks = [self._get_bs4(url) for url in page_urls]
        all_pages_bs4 = await asyncio.gather(*page_tasks)
        print('Páginas obtidas!')
        return [page for page in all_pages_bs4 if page is not None]

    @staticmethod
    def _extract_books_from_pages(pages_bs4: List[BeautifulSoup]) -> List[BeautifulSoup]:
        """Extrai todos os elementos de livros das páginas"""
        all_books = []
        for page_bs4 in pages_bs4:
            books = page_bs4.find_all('article', class_='product_pod')
            all_books.extend(books)
        return all_books

    async def _parse_all_books(self, books_bs4: List[BeautifulSoup]) -> List[List]:
        """Faz o parsing de todos os livros de forma assíncrona"""
        print(f'Parsing de {len(books_bs4)} livros...')
        book_parsing_tasks = [self._parse_book(book) for book in books_bs4]
        return await asyncio.gather(*book_parsing_tasks)

    @staticmethod
    def _save_to_csv(books_data: List[List], csv_path: str):
        """Salva os dados dos livros em um arquivo CSV"""

        csv_file = Path(csv_path).resolve()
        print(f'Escrevendo dados em: {csv_path}')
        print(f'Escrevendo dados em (absoluto): {csv_file}')

        with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([
                'id',
                'title',
                'price',
                'availability',
                'rating',
                'category',
                'image_url',
            ])
            writer.writerows(books_data)

        print(f'Escrita concluída em: {csv_path}')
        csvfile.close()

    async def run(self):
        """
        Método principal
        Inicia o scraping de TARGET_URL
        """
        self.semaphore = asyncio.Semaphore(self.max_concurrent_requests)
        retry_options = ExponentialRetry(attempts=5, statuses={500, 502, 503, 504})

        async with RetryClient(retry_options=retry_options) as self.session:
            self.session._client.headers.update(HEADERS)
            total_pages = await self._get_total_pages()
            page_urls = self._generate_page_urls(total_pages)
            pages_bs4 = await self._fetch_all_pages(page_urls)
            books_bs4 = self._extract_books_from_pages(pages_bs4)
            books_data = await self._parse_all_books(books_bs4)
            self._save_to_csv(books_data, self.OUTPUT_CSV_FILE)

        # permitir que a limpeza do aiohttp seja concluída sem erros.
        # se for windows, ele não esperar o aiohttp encerrar os trabalhos rsr
        await asyncio.sleep(0.5)


if __name__ == '__main__':
    if os.name == 'nt':
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

    start_time = time.time()
    scraper = AsyncBookScraper()
    asyncio.run(scraper.run())
    duration = time.time() - start_time
    print(f'\nTempo total de execução: {duration:.2f} segundos')
