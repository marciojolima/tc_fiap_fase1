from http import HTTPStatus

import pytest

from api_books.security.crypt import get_hash_from_password


@pytest.mark.skipif(condition=True, reason='processamento pesado')
def test_scraping_trigger_suceess(client, fake_users_in_db):
    # Arrange
    username = 'newuser'
    plain_password = 'secret'
    hashed_password = get_hash_from_password(plain_password)
    fake_users_in_db(count=1, exclude={}, username=username, password=hashed_password)

    # Act
    response = client.post(
        '/api/v1/auth/token',
        data={'username': username, 'password': plain_password},
    )
    token = response.json()['access_token']
    response = client.post('api/v1/scraping/trigger', headers={'Authorization': f'Bearer {token}'})
    # Assert
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {'message': 'Data updated successfully'}
