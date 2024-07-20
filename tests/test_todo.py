from http import HTTPStatus

from tests.conftest import TodoFactory


def test_create_todo(client, token):
    response = client.post(
        "/todos/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "title": "Test Todo",
            "description": "Test todo description",
            "state": "draft",
        },
    )
    assert response.json() == {
        "id": 1,
        "title": "Test Todo",
        "description": "Test todo description",
        "state": "draft",
    }


def test_list_todos_should_return_5_todos(session, client, user, token):
    expected_todos = 5
    session.bulk_save_objects(TodoFactory.create_batch(5, user_id=user.id))
    session.commit()
    response = client.get(
        "/todos/",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert len(response.json()["todos"]) == expected_todos


def test_delete_todo(session, client, user, token):
    todo = TodoFactory(user_id=user.id)

    session.add(todo)
    session.commit()

    response = client.delete(
        f"/todos/{todo.id}", headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "message": "Task has been deleted successfully."
    }


def test_delete_todo_error(client, token):
    response = client.delete(
        f"/todos/{10}", headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "Task not found."}


def test_patch_todo_error(client, token):
    response = client.patch(
        "/todos/10",
        json={},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "Task not found."}


def test_patch_todo(session, client, user, token):
    todo = TodoFactory(user_id=user.id)

    session.add(todo)
    session.commit()

    response = client.patch(
        f"/todos/{todo.id}",
        json={"title": "teste!"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json()["title"] == "teste!"
