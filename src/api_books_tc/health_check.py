from fastapi import Depends
from sqlalchemy import text
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session

from api_books_tc.database.connection import get_session


class HeathAPI:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session
        self.api_status = 'up'
        self.db_status = 'up'
        self.db_error = ''

    def check_db(self) -> bool:
        try:
            self.session.execute(text('SELECT 1'))
            self.db_status = 'up'
            return True
        except OperationalError as e:
            self.db_status = 'down'
            self.db_error = str(e)
            return False

    def check_external_service():
        pass
