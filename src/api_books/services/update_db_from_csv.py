import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError, ProgrammingError
from sqlalchemy.orm import sessionmaker

from api_books.models import Book
from api_books.settings import Settings


def update_db():
    df = pd.read_csv(Settings().CSV_PATH, header=0)
    engine_conn = create_engine(Settings().DATABASE_URL)
    Session = sessionmaker(bind=engine_conn)

    try:
        with Session() as session:
            # limpa tabela
            session.query(Book).delete()
            print('Removendo dados anteriores...')

            # Novos dados
            records = df.to_dict('records')
            session.bulk_insert_mappings(Book, records)
            session.commit()
            print('Dados atualizados com sucesso!')
    except (OperationalError, ProgrammingError) as e:
        if 'no such table' in str(e).lower() or "table doesn't exist" in str(e).lower():
            print("Erro: Tabela 'books' não existe.")
            print('Execute as migrações do Alembic primeiro: alembic upgrade head')
        else:
            print(f'Erro de banco de dados: {e}')


if __name__ == '__main__':
    update_db()
