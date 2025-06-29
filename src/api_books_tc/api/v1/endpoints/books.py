from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from api_books_tc.database import get_session
from api_books_tc.models import Book
from api_books_tc.schemas import BookSchema, BooksList, FilterBook

router = APIRouter(prefix='/api/v1/books', tags=['Books'])

FilterQueryBooks = Annotated[FilterBook, Query()]
SessionAnno = Annotated[Session, Depends(get_session)]


@router.get('/', status_code=HTTPStatus.OK, response_model=BooksList)
def get_books(session: SessionAnno, param_request: FilterQueryBooks):
    """
    Os endpoints
    GET /api/v1/books
    GET /api/v1/books/search?title={title}&category={category}
    foram agrupados
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


@router.get('/{book_id}', status_code=HTTPStatus.OK, response_model=BookSchema)
def get_book_by_id(book_id: int, session: SessionAnno):
    """
    Obtém um livro específico pelo seu ID.
    """
    query = select(Book).where(Book.id == book_id)
    book = session.scalar(query)

    return book
