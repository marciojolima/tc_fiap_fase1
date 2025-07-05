import asyncio
from http import HTTPStatus

from fastapi import APIRouter

from api_books_tc.services.scraper import AsyncBookScraper
from api_books_tc.services.update_db_from_csv import update_db

router = APIRouter(prefix='/api/v1/scraping/trigger', tags=['Admin'])


@router.post(
    '/',
    status_code=HTTPStatus.CREATED,
    summary='Iniciar processo de scraping',
    response_description='Confirmação de que o processo de scraping para atualização'
    ' dos dados foi iniciado com sucesso.'
    ' A operação é executada em segundo plano (background).',
)
async def update_csv():
    scrap_services = AsyncBookScraper()
    await scrap_services.run()
    await asyncio.sleep(0.5)
    update_db()

    return {'message': 'success'}
