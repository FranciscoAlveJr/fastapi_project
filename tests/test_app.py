import tracemalloc
from http import HTTPStatus

from fastapi_project.schemas import UserPublic

tracemalloc.start()


def test_root_retorna_ola_mundo(client):
    response = client.get('/')

    assert response.json() == {'message': 'Olá mundo!'}
    assert response.status_code == HTTPStatus.OK


def test_create_user(client):
    response = client.post(
        '/users/',
        json={
            'username': 'jose',
            'email': 'jose@gmail.com',
            'password': 'secret',
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'username': 'jose',
        'email': 'jose@gmail.com',
    }


def test_create_user_name_error(client):
    client.post(
        '/users/',
        json={
            'username': 'jose',
            'email': 'jose@gmail.com',
            'password': 'secret',
        },
    )

    response = client.post(
        '/users/',
        json={
            'username': 'jose',
            'email': 'jose@gmail.com',
            'password': 'secret',
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'User already exists'}


def test_create_user_email_error(client):
    client.post(
        '/users/',
        json={
            'username': 'jose',
            'email': 'jose@gmail.com',
            'password': 'secret',
        },
    )

    response = client.post(
        '/users/',
        json={
            'username': 'maria',
            'email': 'jose@gmail.com',
            'password': 'secret',
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Email already exists'}


def test_read_users(client):
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


def test_read_users_with(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_schema]}


def test_update_user(client):
    client.post(
        '/users/',
        json={
            'username': 'jose',
            'email': 'jose@gmail.com',
            'password': 'secret',
        },
    )

    response = client.put(
        '/users/1',
        json={
            'username': 'maria',
            'email': 'maria@gmail.com',
            'password': 'secret',
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': 1,
        'username': 'maria',
        'email': 'maria@gmail.com',
    }


def test_update_integrity_error(client, user):
    client.post(
        '/users',
        json={
            'username': 'fausto',
            'email': 'fausto@gmail.com',
            'password': 'secret',
        },
    )

    response = client.put(
        f'/users/{user.id}',
        json={
            'username': 'fausto',
            'email': 'junior@gmail.com',
            'password': 'newsecret',
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Username or email already exists'}


def test_delete_user(client, user):
    response = client.delete('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


def test_read_user(client):
    client.post(
        '/users/',
        json={
            'username': 'jose',
            'email': 'jose@gmail.com',
            'password': 'secret',
        },
    )

    response = client.get('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': 1,
        'username': 'jose',
        'email': 'jose@gmail.com',
    }


def test_404_read_user(client):
    response = client.get('/users/2')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_404_update_user(client):
    response = client.put(
        '/users/2',
        json={
            'username': 'maria',
            'email': 'maria@gmail.com',
            'password': 'secret',
        },
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_404_delete_user(client):
    response = client.delete('/users/2')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}
