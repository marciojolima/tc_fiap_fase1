from http import HTTPStatus

import factory


def test_get_books(client, books_dummy, session):
    # Arrange
    count_books = 2
    fake_books = books_dummy(count_books)

    # Act
    response = client.get('/api/v1/books')

    # Assert
    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['books']) == count_books
    assert 'title' in response.json()['books'][0]
    assert fake_books == response.json()['books']


def test_get_books_all_books(client, books_dummy):
    # Arrange
    count_books = 30
    fake_books = books_dummy(count_books)

    # Act
    response = client.get('/api/v1/books')

    # Assert
    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['books']) == count_books
    assert 'title' in response.json()['books'][0]
    assert fake_books == response.json()['books']


def test_get_books_serach_by_category(client, books_dummy):
    # Arrange
    count_books = 10
    fake_books = books_dummy(count_books, category='Poesia')

    # Act
    response = client.get('/api/v1/books/?category=Poesia')

    # Assert
    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['books']) == count_books
    assert 'title' in response.json()['books'][0]
    assert fake_books == response.json()['books']


def test_get_books_serach_by_title(client, books_dummy):
    # Arrange
    count_books = 10
    fake_books = books_dummy(
        count_books, title=factory.Sequence(lambda n: f'titulo Sequencial {n}')
    )

    # Act
    response = client.get('/api/v1/books/?title=titulo Sequencial')

    # Assert
    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['books']) == count_books
    assert 'title' in response.json()['books'][0]
    assert fake_books == response.json()['books']


def test_get_books_by_id(client, books_dummy):
    # Arrange
    fake_books = books_dummy(3)  # noqa

    # Act
    response = client.get('/api/v1/books/2')

    # Assert
    assert response.status_code == HTTPStatus.OK
    assert 'title' in response.json()
    assert 2 == response.json()['id']  # noqa
