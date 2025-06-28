from http import HTTPStatus


def test_get_books(client):
    response = client.get('/api/v1/books')

    assert response.status_code == HTTPStatus.OK
