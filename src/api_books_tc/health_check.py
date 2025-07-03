import httpx
from fastapi import Depends
from sqlalchemy import text
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session

from api_books_tc.database.connection import get_session

EXTERNAL_CONNECTIVITY_TEST_URL = 'https://www.google.com'


class HeathAPI:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session
        self.api_status = 'up'
        self.db_status = 'unknown'
        self.internet_connectivity_status = 'unknown'
        self.db_error = None
        self.internet_connectivity_error = None

    def check_db(self) -> bool:
        """Faz uma consulta teste no banco de dados"""
        try:
            self.session.execute(text('SELECT 1'))
            self.db_status = 'up'
            return True
        except OperationalError as e:
            self.db_status = 'down'
            self.db_error = str(e)
            return False

    def check_internet_connectivity(self) -> bool:
        """Verifica a conectividade externa fazendo uma requisição para um site estável."""
        try:
            # Usamos a nova URL
            response = httpx.get(EXTERNAL_CONNECTIVITY_TEST_URL, timeout=5.0)
            response.raise_for_status()
            self.internet_connectivity_status = 'up'
            return True
        except httpx.RequestError as e:
            self.internet_connectivity_status = 'down'
            self.internet_connectivity_error = f'Erro de conexão: {e.__class__.__name__}'
            return False
        except httpx.HTTPStatusError as e:
            self.internet_connectivity_status = 'down'
            self.internet_connectivity_error = f'Status de erro recebido: {e.response.status_code}'
            return False

    def run_all_checks(self) -> bool:
        """Executa todas as verificações e retorna True se tudo estiver OK."""
        db_ok = self.check_db()
        # Chamamos o método renomeado
        internet_ok = self.check_internet_connectivity()
        return db_ok and internet_ok
