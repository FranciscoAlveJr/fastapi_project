from http import HTTPStatus


def test_root_retorna_ola_mundo(client):
    response = client.get('/')

    assert response.json() == {'message': 'Olá mundo!'}
    assert response.status_code == HTTPStatus.OK


# def test_404_read_user(client, token):
#     response = client.get(
#         '/users/2',
#         headers={'Authorization': f'Bearer {token}'},
#     )

#     assert response.status_code == HTTPStatus.NOT_FOUND
#     assert response.json() == {'detail': 'User not found'}


# def test_404_update_user(client, token):
#     response = client.put(
#         '/users/2',
#         headers={'Authorization': f'Bearer {token}'},
#         json={
#             'username': 'maria',
#             'email': 'maria@gmail.com',
#             'password': 'secret',
#         },
#     )

#     assert response.status_code == HTTPStatus.NOT_FOUND
#     assert response.json() == {'detail': 'User not found'}


# def test_404_delete_user(client):
#     response = client.delete('/users/2')

#     assert response.status_code == HTTPStatus.NOT_FOUND
#     assert response.json() == {'detail': 'User not found'}
