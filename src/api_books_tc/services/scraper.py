import asyncio
import csv
import logging
import os
import re
import time
from typing import Dict, List, Optional

import aiohttp
from aiohttp_retry import ExponentialRetry, RetryClient
from bs4 import BeautifulSoup
from scrapper_exception import PaginatorNotFoundException, ScraperException

TARGET_URL = 'https://books.toscrape.com/'
OUTPUT_CSV_FILE = 'data/books.csv'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    '(KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36 Edg/137.0.0.0'
}


class AsyncBookScraper:
    """Encapsula toda a lógica de scraping do site books.toscrape.com."""

    def __init__(
        self, base_url: str, max_concurrent_requests: int = 15, logger: logging.Logger = None
    ):
        self.base_url = base_url
        self.max_concurrent_requests = max_concurrent_requests
        self.semaphore = asyncio.Semaphore(max_concurrent_requests)
        self.logger = logger
        self.session = None
        self.semaphore = None

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
                return None

    async def _get_total_pages(self) -> int:
        """Encontra e retorna o número total de páginas da paginação do site"""
        # self.logger.info("Buscando o número total de páginas...")
        bs4 = await self._get_bs4(self.base_url)

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

    def _get_book_title(book: BeautifulSoup) -> str:
        return book.h3.a['title']

    def _get_book_price(book: BeautifulSoup) -> float:
        price_text = book.find('p', class_='price_color').text
        pattern = r'\d+(\.\d+)?'
        match = re.search(pattern, price_text)
        return float(match.group(0))

    def _get_book_availability(book: BeautifulSoup) -> bool:
        text = book.find('p', class_='instock availability').text.strip()
        return True if (text == 'In stock') else False

    def _get_book_rating(book: BeautifulSoup) -> str:
        return book.find('p', class_='star-rating')['class'][1]

    async def _get_image_path_and_category(self, url_book_detail: str) -> Dict:
        """Também precisa ser assíncrona"""

        book_detail_bs4 = await self._get_bs4(url_book_detail)
        if not book_detail_bs4:
            raise ScraperException('Não foi possível abrir a página inicial.')

        image_src_value = book_detail_bs4.select_one('.carousel-inner img')['src']
        image_path = image_src_value.replace('../', '')

        category = book_detail_bs4.select('ul.breadcrumb li a')[-1].text.strip()

        return {'image_url': image_path, 'category': category}

    def _get_csv_file_full_path() -> str:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(script_dir)
        return os.path.join(parent_dir, OUTPUT_CSV_FILE)

    async def _parse_book(self, book_bs4) -> Optional[List]:
        title = self._get_book_title(book_bs4)
        price = self._get_book_price(book_bs4)
        availability = self._get_book_availability(book_bs4)
        rating = self._get_book_rating(book_bs4)

        # image and category
        path_book_detail = book_bs4.h3.a['href'].replace('catalogue/', '')
        url_book_detail = TARGET_URL + 'catalogue/' + path_book_detail
        details = await self._get_image_path_and_category(url_book_detail)

        if not details:
            raise ScraperException('Não foi possível abrir a página inicial.')

        return [
            title,
            price,
            availability,
            rating,
            details['category'],
            TARGET_URL + details['image_url'],
        ]

    def _generate_page_urls(total_pages: int) -> List[str]:
        """Gera lista de URLs para todas as páginas de paginação"""
        urls = []
        for page in range(1, total_pages + 1):
            url = f'{TARGET_URL}catalogue/page-{page}.html'
            urls.append(url)
        return urls

    async def _fetch_all_pages(self, page_urls: List[str]) -> List[BeautifulSoup]:
        """Busca todas as páginas de forma assíncrona"""
        print(f'Buscando todas as {len(page_urls)} páginas...')
        page_tasks = [self._get_bs4(url) for url in page_urls]
        all_pages_bs4 = await asyncio.gather(*page_tasks)
        print('Páginas obtidas!')
        return [page for page in all_pages_bs4 if page is not None]

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

    def _save_to_csv(books_data: List[List], csv_path: str):
        """Salva os dados dos livros em um arquivo CSV"""
        print(f'Escrevendo dados em: {csv_path}')

        with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
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

            csv_path = self._get_csv_file_full_path()
            self._save_to_csv(books_data, csv_path)

        # permitir que a limpeza do aiohttp seja concluída sem erros.
        # se for windows, ele não esperar o aiohttp encerrar os trabalhos rsr
        await asyncio.sleep(0.5)


if __name__ == '__main__':
    if os.name == 'nt':
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

    start_time = time.time()
    scraper = AsyncBookScraper(base_url=TARGET_URL)
    asyncio.run(scraper.run())
    duration = time.time() - start_time
    print(f'\nTempo total de execução: {duration:.2f} segundos')
