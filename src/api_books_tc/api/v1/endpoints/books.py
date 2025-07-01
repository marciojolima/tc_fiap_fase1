from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from api_books_tc.database import get_session
from api_books_tc.models import Book
from api_books_tc.schemas import BookSchema, BooksList, CategoriesList, FilterBook, FilterCategory

router = APIRouter(prefix='/api/v1', tags=['Books'])

FilterQueryBooks = Annotated[FilterBook, Query()]
FilterQueryCategories = Annotated[FilterCategory, Query()]
SessionAnno = Annotated[Session, Depends(get_session)]


@router.get('/books', status_code=HTTPStatus.OK, response_model=BooksList)
def get_books(session: SessionAnno, param_request: FilterQueryBooks):
    """
    Os endpoints
    GET /api/v1/books
    GET /api/v1/books/search?title={title}&category={category}
    foram agrupadas? GET /api/v1/books
    """

    query = select(Book)

    if param_request.title:
        query = query.filter(Book.title.contains(param_request.title))

    if param_request.category:
        query = query.filter(Book.category.contains(param_request.category))

    if param_request.offset:
        query = query.offset(param_request.offset)

    if param_request.limit:
        query = query.limit(param_request.limit)

    books = session.scalars(query).all()
    count_books = session.scalar(select(func.count()).select_from(query.subquery()))

    return {'books': books, 'count_books': count_books}


@router.get('/books/{book_id}', status_code=HTTPStatus.OK, response_model=BookSchema)
def get_book_by_id(book_id: int, session: SessionAnno):
    """
    Obtém um livro específico pelo seu ID.
    """
    query = select(Book).where(Book.id == book_id)
    book = session.scalar(query)

    return book


@router.get('/categories/', status_code=HTTPStatus.OK, response_model=CategoriesList)
def get_books_categories(session: SessionAnno, param_request: FilterQueryCategories):
    """
    Obtém todas as categorias dos livros.
    """

    query = select(Book.category).distinct().order_by(Book.category)

    if param_request.name:
        query = query.filter(Book.category.contains(param_request.name))

    categories = session.scalars(query).all()
    count_categories = len(categories)

    return {'categories': categories, 'count_categories': count_categories}
