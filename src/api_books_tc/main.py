from http import HTTPStatus

from fastapi import FastAPI

from api_books_tc.api.v1.endpoints import books, users
from api_books_tc.schemas.basics import Message

app = FastAPI(
    title='Tech Challenge FIAP-6MELT grupo 28',
    description='Api para consumir informações de livros',
    version='1.0.0',
)

app.include_router(books.router)
app.include_router(users.router)


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    """ """
    return {'status': 'API is running!!'}
