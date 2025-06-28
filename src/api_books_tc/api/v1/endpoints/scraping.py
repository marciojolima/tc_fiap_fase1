import asyncio
from http import HTTPStatus

from fastapi import APIRouter

from api_books_tc.services.scraper import AsyncBookScraper
from api_books_tc.services.update_db_from_csv import update_db

router = APIRouter(prefix='/api/v1/scraping/trigger', tags=['ADMIN'])


@router.post('/', status_code=HTTPStatus.OK)
async def update_csv():
    scrap_services = AsyncBookScraper()
    await scrap_services.run()
    await asyncio.sleep(0.5)
    update_db()

    return {'message': 'success'}
