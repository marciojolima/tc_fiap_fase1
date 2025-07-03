from http import HTTPStatus

from api_books_tc.health_check import HeathAPI


def test_get_health_status_is_running(client):
    # Arrange

    # Act
    response = client.get('/api/v1/health/')

    # Assert
    response_body_expected = {
        'api_status': 'up',
        'database': {'status': 'up', 'error': None},
        'internet_connectivity': {'status': 'up', 'error': None},
    }
    assert response.json() == response_body_expected


def test_get_health_must_throw_exception_503(client, app_books, mock_service_health):
    # Arrange
    app_books.dependency_overrides[HeathAPI] = lambda: mock_service_health
    # Act
    response = client.get('/api/v1/health/')

    # Assert
    response_body_expected = {
        'detail': {
            'api_status': 'error',
            'database': {
                'status': 'disconnected',
                'error': 'Connection timeout',
            },
            'internet_connectivity': {
                'status': 'offline',
                'error': 'No internet',
            },
        }
    }
    assert response.status_code == HTTPStatus.SERVICE_UNAVAILABLE
    assert response.json() == response_body_expected
    app_books.dependency_overrides.clear()
