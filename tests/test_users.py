from http import HTTPStatus

import pytest


def test_create_users(client, fake_users):
    # Arrange
    fake_new_users = fake_users(1, exclude_id=False)

    new_user = fake_new_users[0]
    json_post = new_user.copy()
    json_post.pop('id')
    new_user.pop('password')
    # Act
    response = client.post('/api/v1/users', json=json_post)

    # Assert
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == new_user


@pytest.mark.parametrize(
    'params',
    [
        ('email', 'Username already exists'),
        ('username', 'Email already exists'),
    ],
)
def test_create_existing_users_must_be_conflict_username(client, fake_users_in_db, params):
    # Arrange
    attr_to_change, http_message = params

    fake_new_users = fake_users_in_db(1)
    new_user = fake_new_users[0]
    json_post = new_user.copy()
    json_post.pop('id')
    json_post[attr_to_change] = 'diff_' + new_user[attr_to_change]

    # Act
    response = client.post('/api/v1/users', json=json_post)

    # Assert
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': http_message}


def test_get_all_users(client, fake_users_in_db):
    # Arrange
    total = 10
    fake_new_users = fake_users_in_db(total, exclude={'password'})

    # Act
    response = client.get('/api/v1/users')

    # Assert
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'total': total, 'users': fake_new_users}
