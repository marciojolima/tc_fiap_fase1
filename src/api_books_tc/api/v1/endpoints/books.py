from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Query

from api_books_tc.schemas import BookBase, FilterBook

router = APIRouter(prefix='/api/v1/books', tags=['Books'])

FilterQueryBooks = Annotated[FilterBook, Query()]
# DataBase = Annotated[DataBaseManager, Depends()]


@router.get('/', status_code=HTTPStatus.OK, response_model=BookBase)
async def get_books(db, filter: FilterQueryBooks):
    """
    Endpoint de exemplo que retorna uma mensagem simples.
    Este será o nosso "Hello World" para a rota de livros.
    """

    return {'message': 'Ola book!'}
