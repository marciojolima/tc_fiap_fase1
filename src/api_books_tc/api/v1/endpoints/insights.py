from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, Query

from api_books_tc.database.books import BookDataBase
from api_books_tc.schemas import BooksList, FilterPage

router = APIRouter(prefix='/api/v1/insights', tags=['Insights'])

DBService = Annotated[BookDataBase, Depends()]
FilterQueryPage = Annotated[FilterPage, Query()]


@router.get('/top-rated/', status_code=HTTPStatus.OK, response_model=BooksList)
def get_books_top_rated(db: DBService, param_request: FilterQueryPage):
    """Obtém todos os livros por ordem dos mais bem avaliadaos"""
    count_books, books = db.get_books_top_rated(
        offset=param_request.offset, limit=param_request.limit
    )

    return {'books': books, 'total': count_books}
