from http import HTTPStatus


def test_root_endpoint_deve_retornar_is_running(client):
    response = client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'message': 'Bem-vindo à API',
        'api': 'Books API - FIAP - Tech Challenge ',
        'version': 'v1',
        'status': 'running',
        'description': 'Acesse /docs para ver a documentação interativa.',
    }
