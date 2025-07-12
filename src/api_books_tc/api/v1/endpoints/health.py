from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from api_books_tc.health_check import HeathAPI
from api_books_tc.schemas import RespostaHealthCheck

router = APIRouter(tags=['Monitoring'])

HealthService = Annotated[HeathAPI, Depends()]


@router.get(
    '/api/v1/health',
    tags=['Monitoring'],
    summary='Verifica a saúde da API',
    response_description='Retorna o status da API e do banco de dados',
    response_model=RespostaHealthCheck,
)
def get_health_status(hc: HealthService):
    """
    Retorna o status da API e do banco de dados
    """
    is_healthy = hc.run_all_checks()

    response_body = {
        'api_status': hc.api_status,
        'database': {
            'status': hc.db_status,
            'error': hc.db_error,
        },
        'internet_connectivity': {
            'status': hc.internet_connectivity_status,
            'error': hc.internet_connectivity_error,
        },
    }

    if not is_healthy:
        raise HTTPException(
            status_code=HTTPStatus.SERVICE_UNAVAILABLE,
            detail=response_body,
        )

    return response_body
