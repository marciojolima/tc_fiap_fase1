import pandas as pd
from sqlalchemy import create_engine

from ..settings import Settings


def update_db():
    df = pd.read_csv(Settings().CSV_PATH)
    engine_conn = create_engine(Settings().DATABASE_URL)
    df.to_sql('books', engine_conn, if_exists='replace', index=False)


if __name__ == '__main__':
    update_db()
    print('DataBase books.db criado com sucesso!')
