import asyncio
from http import HTTPStatus

from fastapi import APIRouter, Depends

from api_books.security.auth import get_user_tokenizer
from api_books.services.scraper import AsyncBookScraper
from api_books.services.update_db_from_csv import update_db

router = APIRouter(prefix='/api/v1/scraping', tags=['Admin'])


@router.post(
    '/trigger',
    status_code=HTTPStatus.CREATED,
    summary='Iniciar processo de scraping (requer autenticação)',
    response_description='Confirmação de que o processo de scraping para atualização'
    ' dos dados foi iniciado com sucesso.'
    ' A operação é executada em segundo plano (background).',
)
async def update_csv_db(authorized_user=Depends(get_user_tokenizer)):
    """
    Este é um endpoint protegido que inicia o processo de web scraping
    do site 'books.toscrape.com' para atualizar a base de dados.
    """
    scrap_services = AsyncBookScraper()
    await scrap_services.run()
    await asyncio.sleep(0.5)
    update_db()

    return {'message': 'Data updated successfully'}
