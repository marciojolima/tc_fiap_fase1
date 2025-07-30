import time

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from api_books.logging_config import app_logger


class LoggingMiddleware(BaseHTTPMiddleware):
    @staticmethod
    async def dispatch(request: Request, call_next):
        start_time = time.time()

        # Processa a requisição para obter a resposta
        response = await call_next(request)

        process_time = (time.time() - start_time) * 1000

        # O `contextualize` é a forma do Loguru de adicionar dados extras
        with app_logger.contextualize(
            ip=request.client.host,
            method=request.method,
            url=str(request.url),
            status_code=response.status_code,
            process_time=process_time,
        ):
            app_logger.info('Request handled')

        return response
