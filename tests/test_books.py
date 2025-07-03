from http import HTTPStatus

from factory import Iterator


def test_get_books(client, books_dummy_in_db):
    # Arrange
    count_books = 3
    fake_books = books_dummy_in_db(count_books)
    # Act
    response = client.get('/api/v1/books')
    # Assert
    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['books']) == count_books
    assert 'title' in response.json()['books'][0]
    assert fake_books == response.json()['books']


def test_get_all_books(client, books_dummy_in_db):
    # Arrange
    count_books = 30
    fake_books = books_dummy_in_db(count_books)
    # Act
    response = client.get('/api/v1/books')
    # Assert
    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['books']) == count_books
    assert 'title' in response.json()['books'][0]
    assert fake_books == response.json()['books']


def test_get_books_top_rated(client, books_dummy_in_db):
    # Arrange

    rates = [i for i in range(1, 6) for _ in range(2)]
    # [1, 1, 2, 2, 3, 3, 4, 4, 5, 5]
    count_books = len(rates)

    books_dummy_in_db(count_books, rating=Iterator(rates))
    # Act
    response = client.get(f'/api/v1/books/top-rated/?limit={count_books - 2}')

    # Assert
    assert response.status_code == HTTPStatus.OK
    assert 'rating' in response.json()['books'][0]
    assert 5.0 == response.json()['books'][0]['rating']  # noqa
    assert 2.0 == response.json()['books'][7]['rating']  # noqa


def test_get_books_serach_by_category(client, books_dummy_in_db):
    # Arrange
    count_books = 10
    fake_books = books_dummy_in_db(count_books, category='Poesia')
    # Act
    response = client.get('/api/v1/books/?category=Poesia')
    # Assert
    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['books']) == count_books
    assert 'title' in response.json()['books'][0]
    assert fake_books == response.json()['books']


def test_get_books_search_by_title(client, books_dummy_in_db):
    # Arrange
    count_books = 10
    start_n = 1
    titles = [f'titulo Sequencial {i + start_n}' for i in range(count_books)]
    books_dummy_in_db(count_books, title=Iterator(titles))
    # Act
    response = client.get('/api/v1/books/?title=titulo Sequencial 3')
    # Assert
    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['books']) == 1
    assert 'title' in response.json()['books'][0]


def test_get_books_pagination_limit_and_offset(client, books_dummy_in_db):
    # Arrange
    count_books = 30
    limit = 3
    offset = 20
    books_dummy_in_db(count_books)
    # Act
    endpoint = f'/api/v1/books/?limit={limit}&offset={offset}'
    response = client.get(endpoint)
    last_item_id = response.json()['books'][limit - 1]['id']
    # Assert
    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['books']) == limit
    assert 'title' in response.json()['books'][0]
    assert (limit + offset) == last_item_id


def test_get_books_by_id(client, books_dummy_in_db):
    # Arrange
    books_dummy_in_db(3)  # noqa
    # Act
    response = client.get('/api/v1/books/2')
    # Assert
    assert response.status_code == HTTPStatus.OK
    assert 'title' in response.json()
    assert 2 == response.json()['id']  # noqa


def test_get_books_by_id_must_throw_not_found(client, books_dummy_in_db):
    # Arrange
    books_dummy_in_db(3)  # noqa
    # Act
    response = client.get('/api/v1/books/-1')
    # Assert
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_get_categories(client, books_dummy_in_db, session):
    # Arrange
    count_books = 12
    choices = ['Childhood', 'Childrens', 'Fantasy', 'Fiction', 'Mystery', 'Sci-Fi']
    categories_dummies = Iterator(choices)
    books_dummy_in_db(count_books, category=categories_dummies)

    # Act
    response = client.get('/api/v1/categories')

    # Assert
    assert response.status_code == HTTPStatus.OK
    assert len(choices) == response.json()['total']
    assert choices == response.json()['categories']


def test_get_categorie_filter_by_name(client, books_dummy_in_db, session):
    # Arrange
    count_books = 12
    choices = ['Childhood', 'Childrens', 'Fantasy', 'Fiction', 'Mystery', 'Sci-Fi']
    categories_dummies = Iterator(choices)
    books_dummy_in_db(count_books, category=categories_dummies)

    # Act
    response = client.get('/api/v1/categories/?name=Child')

    # Assert
    assert response.status_code == HTTPStatus.OK
    assert 2 == response.json()['total']  # noqa
