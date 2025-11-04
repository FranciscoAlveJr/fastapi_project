from fastapi.testclient import TestClient

from fastapi_project.app import app


def test_root_retorna_ola_mundo():
    client = TestClient(app)

    response = client.get('/')

    assert response.json() == {'message': 'Olá mundo!'}
    assert response.status_code == 200
