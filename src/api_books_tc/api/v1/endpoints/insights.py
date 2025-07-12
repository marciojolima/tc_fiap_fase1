from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, Query

from api_books_tc.database.books import BookDataBase
from api_books_tc.schemas import (
    BooksList,
    FilterPage,
    FilterStatPriceRange,
    StatsCategories,
    StatsOverview,
    StatsPriceRange,
)

router = APIRouter(prefix='/api/v1/stats', tags=['Insights'])

DBService = Annotated[BookDataBase, Depends()]
FilterQueryPage = Annotated[FilterPage, Query()]
FilterPriceRange = Annotated[FilterStatPriceRange, Query()]


@router.get(
    '/overview/',
    status_code=HTTPStatus.OK,
    response_model=StatsOverview,
    summary='Fornece um resumo estatístico da coleção de livros.',
)
def get_books_stats_overview(db: DBService):
    """Estatísticas  gerais  da  coleção  (total  de livros,
    preço médio, distribuição de ratings)"""

    total_books, avg_price, rating_dist = db.get_stats_overview()
    rating_distribution = {rating: count for rating, count in rating_dist}
    return {
        'total_books': total_books,
        'average_price': avg_price,
        'rating_distribuition': rating_distribution,
    }


@router.get(
    '/top-rated/',
    status_code=HTTPStatus.OK,
    response_model=BooksList,
    summary='Obtém todos os livros por ordem dos mais bem avaliadaos',
)
def get_books_top_rated(db: DBService, param_request: FilterQueryPage):
    total_books, books = db.get_books_top_rated(
        offset=param_request.offset, limit=param_request.limit
    )

    return {'total': total_books, 'books': books}


@router.get(
    '/price-range/',
    status_code=HTTPStatus.OK,
    response_model=StatsPriceRange,
    summary='Distribuição de preços por categoria',
)
def get_books_stats_price_range(db: DBService, param_request: FilterPriceRange):
    total_books, books = db.get_stats_by_price_range(
        min_price=param_request.min_price, max_price=param_request.max_price
    )

    return {'total': total_books, 'books': books}


@router.get(
    '/categories/',
    status_code=HTTPStatus.OK,
    response_model=StatsCategories,
    summary='Lista todas as categorias de livros.',
)
def get_categories_stats_overview(db: DBService):
    """
    Retorna uma lista de strings, onde cada string é uma categoria única
    """

    total_categories, categories_count_dist, categories_price_dist = db.get_stats_categories()

    categories_count_distribution = {category: count for category, count in categories_count_dist}

    categories_avg_price_distribution = {
        category: price for category, price in categories_price_dist
    }

    return {
        'total_categories': total_categories,
        'categories_count_distribution': categories_count_distribution,
        'categories_avg_price_distribution': categories_avg_price_distribution,
    }
