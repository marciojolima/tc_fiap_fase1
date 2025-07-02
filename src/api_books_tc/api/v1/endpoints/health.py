from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from api_books_tc.health_check import HeathAPI

router = APIRouter(tags=['Monitoring'])

HealthService = Annotated[HeathAPI, Depends()]


@router.get(
    '/api/v1/health',
    tags=['Monitoring'],
    summary='Verifica a saúde da API e a conexão com o banco de dados',
    response_description='Retorna o status da API e do banco de dados',
)
def get_health_status(hc: HealthService):
    if not hc.check_db():
        raise HTTPException(
            status_code=HTTPStatus.SERVICE_UNAVAILABLE,
            detail={
                'api_status': hc.api_status,
                'database_status': hc.db_status,
                'database_error': f'Erro de conexão com o banco de dados {hc.db_error}',
            },
        )

    return {'api_status': hc.api_status, 'database_status': hc.db_status}
