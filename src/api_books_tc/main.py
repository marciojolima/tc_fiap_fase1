from http import HTTPStatus

from fastapi import FastAPI

from api_books_tc.api.v1.endpoints import auth, books, health, insights, scraping, users
from api_books_tc.schemas import MessageStatus

app = FastAPI(
    title='Tech Challenge FIAP-6MELT grupo 28',
    description='Api para consumir informações de livros',
    version='1.0.0',
)

app.include_router(books.router)
app.include_router(users.router)
app.include_router(scraping.router)
app.include_router(health.router)
app.include_router(auth.router)
app.include_router(insights.router)


@app.get(
    '/',
    status_code=HTTPStatus.OK,
    response_model=MessageStatus,
    tags=['Root'],
    summary='Página Inicial da API.',
)
def read_root():
    """Endpoint de status"""
    return {
        'message': 'Bem-vindo à API',
        'api': 'Books API - FIAP - Tech Challenge ',
        'version': 'v1',
        'status': 'running',
        'description': 'Acesse /docs para ver a documentação interativa.',
    }
