import os
from http import HTTPStatus

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse

from api_books.endpoints import auth, books, health, insights, ml, scraping, users
from api_books.middlewares.logging import LoggingMiddleware
from api_books.schemas import MessageStatus

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
app.include_router(ml.router)

# Logs
app.add_middleware(LoggingMiddleware)


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


@app.get(
    '/api/v1/download/books',
    status_code=HTTPStatus.OK,
    tags=['Download'],
    summary='Faz o download do arquivo .csv contendo todos os livros cadastrados',
)
def download_books():
    file_path = 'data/books.csv'

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail='Arquivo não encontrado')

    return FileResponse(
        path=file_path,
        filename='books.csv',
        media_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename=books.csv'},
    )
