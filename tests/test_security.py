from http import HTTPStatus

from jwt import decode

from api_books_tc.security.auth import create_jwt
from api_books_tc.security.crypt import get_hash_from_password
from api_books_tc.settings import Settings


def test_jwt():
    claim = {'test': 'test'}

    token = create_jwt(claim)

    jwt_decoded = decode(jwt=token, key=Settings().SECRET_KEY, algorithms=Settings().ALGORITHM)

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
        '/api/v1/auth/token', data={'username': username, 'password': plain_password}
    )
    token = response.json()

    # Assert
    assert response.status_code == HTTPStatus.OK
    assert token['token_type'] == 'bearer'
    assert 'access_token' in token
