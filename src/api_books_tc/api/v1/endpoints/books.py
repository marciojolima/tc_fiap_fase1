from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query

from api_books_tc.database.books import BookDataBase
from api_books_tc.schemas import (
    BookSchema,
    BooksList,
    CategoriesList,
    FilterBook,
    FilterCategory,
    FilterPage,
)

router = APIRouter(prefix='/api/v1', tags=['Books'])

FilterQueryBooks = Annotated[FilterBook, Query()]
FilterQueryCategories = Annotated[FilterCategory, Query()]
FilterQueryPage = Annotated[FilterPage, Query()]
DBService = Annotated[BookDataBase, Depends()]


@router.get(
    '/books/',
    status_code=HTTPStatus.OK,
    response_model=BooksList,
    summary='Lista todos os livros disponíveis (Filtro opcional por título ou categoria).',
)
def get_books(db: DBService, param_request: FilterQueryBooks):
    """
    Obs.: A rota "GET /api/v1/books/search?title={title}&category={category}'
    '" está inclusa neste endpoint.

    Obtém todos os livros com opção de filtro pelos parâmetros title e category.
    """

    count_books, books = db.get_books(
        title=param_request.title,
        category=param_request.category,
        offset=param_request.offset,
        limit=param_request.limit,
    )

    return {'books': books, 'total': count_books}


@router.get(
    '/books/{book_id}',
    status_code=HTTPStatus.OK,
    response_model=BookSchema,
    summary='Busca um único livro pelo seu ID.',
)
def get_book_by_id(book_id: int, db: DBService):
    try:
        if book_id <= 0:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST, detail='id should be a positive number'
            )

        book = db.get_book_by_id(book_id)
    except ValueError:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Not found')

    return book


@router.get(
    '/categories/',
    status_code=HTTPStatus.OK,
    response_model=CategoriesList,
    summary='Lista todas as categorias de livros existentes.',
)
def get_books_categories(db: DBService, param_request: FilterQueryCategories):
    """
    Retorna uma lista de strings, onde cada string é uma categoria única
    """
    if not param_request.name:
        param_request.name = ''
    count_categories, categories = db.get_categories(param_request.name)

    return {'categories': categories, 'total': count_categories}
