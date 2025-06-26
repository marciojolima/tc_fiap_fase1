from http import HTTPStatus

from fastapi import APIRouter

router = APIRouter(prefix='/api/v1/books', tags=['Books'])


@router.get('/', status_code=HTTPStatus.OK)
async def get_hello_world_book():
    """
    Endpoint de exemplo que retorna uma mensagem simples.
    Este será o nosso "Hello World" para a rota de livros.
    """
    return {'message': 'Ola book!'}
