from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.exc import OperationalError

from api_books_tc.database.books import BookDataBase

router = APIRouter(tags=['Monitoring'])

DBService = Annotated[BookDataBase, Depends()]


@router.get(
    '/api/v1/health',
    tags=['Monitoring'],
    summary='Verifica a saúde da API e a conexão com o banco de dados',
    response_description='Retorna o status da API e do banco de dados',
)
def get_health_status(db: DBService):
    api_status = 'ok'
    db_status = 'ok'

    try:
        db.session.execute(text('SELECT 1'))
    except OperationalError as e:
        raise HTTPException(
            status_code=HTTPStatus.SERVICE_UNAVAILABLE,
            detail={
                'api_status': api_status,
                'database_status': db_status,
                'database_error': f'Erro de conexão com o banco de dados: {e}',
            },
        )

    return {'api_status': api_status, 'database_status': db_status}
