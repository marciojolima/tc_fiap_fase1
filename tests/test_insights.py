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
