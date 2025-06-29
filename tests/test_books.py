from http import HTTPStatus


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
