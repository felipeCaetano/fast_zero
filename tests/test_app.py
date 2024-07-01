from http import HTTPStatus


def test_read_root_deve_retornar_ok_e_ola_mundo(client):
    response = client.get("/")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"message": "Olá, mundo!"}


def test_create_user(client):
    response = client.post(
        "/users/",
        json={
            "username": "testusername",
            "password": "password",
            "email": "test@test.com",
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        "username": "testusername",
        "email": "test@test.com",
        "id": 1,
    }


def test_read_users(client):
    response = client.get("/users/")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "users": [
            {
                "username": "testusername",
                "email": "test@test.com",
                "id": 1,
            }
        ]
    }


def test_update_user(client):
    response = client.put(
        "/users/1",
        json={
            "username": "testuser",
            "email": "test@test.com",
            "password": "123",
            "id": 1,
        },
    )
    assert response.json() == {
        "username": "testuser",
        "email": "test@test.com",
        "id": 1,
    }


def test_update_user_retorna_404(client):
    response = client.put(
        "/users/2",
        json={
            "username": "testuser",
            "email": "test@test.com",
            "password": "123",
            "id": 1,
        },
    )
    assert response.json() == {"detail": "User not found"}


def test_delete_user(client):
    response = client.delete("/users/1")
    assert response.json() == {"message": "User deleted."}


def test_delete_user_retorna_404(client):
    response = client.delete("/users/2")
    assert response.json() == {"detail": "User not found"}
