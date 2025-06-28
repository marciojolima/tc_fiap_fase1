import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from api_books_tc.settings import Settings

df = pd.read_csv(Settings().CSV_PATH)
engine_conn = create_engine(Settings().DATABASE_URL)
df.to_sql('books', engine_conn, if_exists='replace', index=False)


def get_session():  # pragma: no cover
    with Session(engine_conn) as session:
        yield session
