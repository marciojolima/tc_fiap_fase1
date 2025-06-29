from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import sessionmaker

from api_books_tc.database import get_session
from api_books_tc.main import app
from api_books_tc.models import table_registry
from api_books_tc.schemas import BookSchema
from tests.dummy_factory import BookFactory


@pytest.fixture
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()


# Apenas uma vez por execução de testes
@pytest.fixture(scope='session')
def engine():
    """Cria um engine SQLite em memória para toda a sessão de testes."""
    return create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )


# Executa para cada função de teste
@pytest.fixture
def tables(engine):
    """Cria as tabelas antes de cada teste e as derruba depois."""
    table_registry.metadata.create_all(engine)
    yield
    table_registry.metadata.drop_all(engine)


@pytest.fixture
def session(engine, tables):
    """
    Cria uma nova sessão para um teste, garantindo o isolamento.
    Usa a fixture 'tables' para garantir que as tabelas existam.
    """
    # Cria uma conexão para a duração do teste
    with engine.connect() as connection:
        transaction = connection.begin()
        Session = sessionmaker(bind=connection)
        session = Session()

        try:
            yield session
        finally:
            session.close()
            transaction.rollback()


@pytest.fixture
def books_dummy(session):
    def _create_books(count: int, **kwargs):
        BookFactory._meta.sqlalchemy_session = session
        BookFactory._meta.sqlalchemy_session_persistence = 'commit'

        books = list(BookFactory.create_batch(count, **kwargs))
        books_dict = [BookSchema.model_validate(book).model_dump() for book in books]
        return books_dict

    return _create_books
