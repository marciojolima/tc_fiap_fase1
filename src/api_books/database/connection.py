from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from api_books.settings import Settings

engine_conn = create_engine(Settings().DATABASE_URL)


def get_session():  # pragma: no cover
    with Session(engine_conn) as session:
        yield session
