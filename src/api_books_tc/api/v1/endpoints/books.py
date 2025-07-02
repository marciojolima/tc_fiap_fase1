from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query

from api_books_tc.database.books import BookDataBase
from api_books_tc.schemas import BookSchema, BooksList, CategoriesList, FilterBook, FilterCategory

router = APIRouter(prefix='/api/v1', tags=['Books'])

FilterQueryBooks = Annotated[FilterBook, Query()]
FilterQueryCategories = Annotated[FilterCategory, Query()]
DBService = Annotated[BookDataBase, Depends()]


@router.get(
    '/books/',
    status_code=HTTPStatus.OK,
    response_model=BooksList,
    summary='Obs.: A rota "GET /api/v1/books/search?title={title}&category={category}'
    '" está inclusa neste endpoint.',
)
def get_books(db: DBService, param_request: FilterQueryBooks):
    """
    Obtém todos os livros com opção de filtro pelos parâmetros title e category.
    """

    count_books, books = db.get_books(
        title=param_request.title,
        category=param_request.category,
        limit=param_request.limit,
        offset=param_request.offset,
    )

    return {'books': books, 'total': count_books}


@router.get('/books/{book_id}', status_code=HTTPStatus.OK, response_model=BookSchema)
def get_book_by_id(book_id: int, db: DBService):
    """
    Obtém um livro específico pelo seu ID.
    """

    try:
        book = db.get_book_by_id(book_id)
    except ValueError:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Not found')

    return book


@router.get('/books/top-rated/', status_code=HTTPStatus.OK, response_model=BooksList)
def get_books_top_rated(db: DBService):
    """
    Obtém todos os livros por ordem dos mais bem avaliadaos
    """

    count_books, books = db.get_books_top_rated()

    return {'books': books, 'total': count_books}


@router.get('/categories/', status_code=HTTPStatus.OK, response_model=CategoriesList)
def get_books_categories(db: DBService, param_request: FilterQueryCategories):
    """
    Obtém todas as categorias dos livros.
    """

    count_categories, categories = db.get_categories(param_request.name)

    return {'categories': categories, 'total': count_categories}
