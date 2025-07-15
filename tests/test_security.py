from http import HTTPStatus

import pytest
from jwt import decode

from api_books.security.auth import create_jwt
from api_books.security.crypt import get_hash_from_password
from api_books.settings import Settings

settings = Settings()


def test_jwt():
    # Arrange
    claim = {'test': 'test'}

    # Act
    token = create_jwt(claim)
    jwt_decoded = decode(jwt=token, key=settings.SECRET_KEY, algorithms=settings.ALGORITHM)

    # Assert
    assert jwt_decoded['test'] == claim['test']
    assert 'exp' in jwt_decoded


def test_get_token(client, fake_users_in_db):
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
    token = response.json()

    # Assert
    assert response.status_code == HTTPStatus.OK
    assert token['token_type'] == 'bearer'
    assert 'access_token' in token


@pytest.mark.parametrize(
    'params',
    [
        ('newuser', 'wronguser', 'secret', 'secret', 'username not found'),
        ('newuser', 'newuser', 'secret', 'wrongsecret', 'Incorrect password'),
    ],
)
def test_get_token_invalid_user_or_password(client, fake_users_in_db, params):
    # Arrange
    username, request_username, plain_password, request_plain_password, detail = params

    # username = 'newuser'
    # plain_password = 'secret'
    hashed_password = get_hash_from_password(plain_password)
    fake_users_in_db(count=1, exclude={}, username=username, password=hashed_password)

    # Act
    response = client.post(
        '/api/v1/auth/token',
        data={'username': request_username, 'password': request_plain_password},
    )

    # Assert
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': detail}


def test_jwt_invalid_token(client):
    # Arrange
    # Act
    response = client.post(
        '/api/v1/scraping/trigger',
        headers={'Authorization': 'Bearer texto qualquer para invalidar'},
    )
    # Assert
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_jwt_expired_token(client):
    # Arrange
    expired_token = (
        'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.'
        'eyJzdWIiOiJtYXJjaW8iLCJleHAiOjB9.'
        '53Fy2m1goFZ5-_APdDhKxSscsnIOnqebjQSo4J1bv58'
    )

    # Act
    response = client.post(
        '/api/v1/scraping/trigger',
        headers={'Authorization': f'Bearer {expired_token}'},
    )

    # Assert
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Expired token'}
