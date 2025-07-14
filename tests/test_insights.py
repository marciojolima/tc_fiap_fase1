from http import HTTPStatus

from factory import Iterator


def test_get_books_top_rated(client, fake_books_in_db):
    # Arrange

    rates = [i for i in range(1, 6) for _ in range(2)]
    # [1, 1, 2, 2, 3, 3, 4, 4, 5, 5]
    count_books = len(rates)

    fake_books_in_db(count_books, rating=Iterator(rates))
    # Act
    response = client.get(f'/api/v1/stats/top-rated/?limit={count_books - 2}')

    # Assert
    assert response.status_code == HTTPStatus.OK
    assert 'rating' in response.json()['books'][0]
    assert 5.0 == response.json()['books'][0]['rating']  # noqa
    assert 2.0 == response.json()['books'][7]['rating']  # noqa


def test_get_stats_books_overview(client, fake_books_in_db):
    # Arrange
    prices = [10.0, 15.0, 10.0, 15.0]
    rates = [5.0, 5.0, 5.0, 4.0]
    categories = ['A', 'B', 'B', 'B']
    fake_books_in_db(
        4, rating=Iterator(rates), price=Iterator(prices), category=Iterator(categories)
    )

    # Act
    response = client.get('api/v1/stats/overview/')
    json_expect_response = {
        'total_books': 4,
        'average_price': 12.5,
        'count_categories': 2,
        'rating_distribuition': {'4.0': 1, '5.0': 3},
    }

    # Assert
    assert response.status_code == HTTPStatus.OK
    assert response.json() == json_expect_response


def test_get_stats_books_price_range(client, fake_books_in_db):
    # Arrange
    prices = [10.0, 10.24, 10.25, 12.0, 18.30, 22.0, 25.0, 29.80]
    books = fake_books_in_db(8, price=Iterator(prices))
    books_ranged = books[2:7]  # posicao de 2 até 6

    # Act
    response = client.get('api/v1/stats/price-range/?min_price=10.25&max_price=25.0')
    json_expect_response = {'total': 5, 'books': books_ranged}

    # Assert
    assert response.status_code == HTTPStatus.OK
    assert response.json() == json_expect_response


def test_get_stats_categories_books(client, fake_books_in_db):
    # Arrange
    categories = ['Fiction', 'Children', 'Fiction', 'Children', 'Fiction']
    prices = [12.0, 8.0, 18.0, 10.0, 12.0]
    fake_books_in_db(5, category=Iterator(categories), price=Iterator(prices))

    # Act
    response = client.get('api/v1/stats/categories')
    json_expect_response = {
        'total_categories': 2,
        'categories_count_distribution': {'Children': 2, 'Fiction': 3},
        'categories_avg_price_distribution': {'Children': 9.0, 'Fiction': 14.0},
    }

    # Assert
    assert response.status_code == HTTPStatus.OK
    assert response.json() == json_expect_response
