import logging

import django
import pytest

django.setup()
logger = logging.getLogger(__name__)


@pytest.mark.django_db
def test_login_success(api_client, user, user_login_data) -> None:
    response_login = api_client.post("/api/login/", data=user_login_data, format="json")
    assert response_login.json().get('token')


@pytest.mark.django_db
def test_login_fail(api_client, user) -> None:
    response_login = api_client.post("/api/login/", data={"user": "admin", "password": "password"}, format="json")
    assert response_login.status_code == 400


@pytest.mark.django_db
def test_create_task_by_unauthorized_user_success(api_client, task_data) -> None:
    # Create a task  
    response_create = api_client.post("/api/tasks/", data=task_data, format="json")
    response_data = response_create.json()
    assert response_create.status_code == 201
    assert response_data.get('title') == task_data["title"]

    # Read the task  
    response_read = api_client.get(f"/api/tasks/{response_data.get('id')}/", format="json")
    assert response_read.status_code == 200
    assert response_data.get('title') == task_data["title"]


@pytest.mark.django_db
def test_create_task_by_authorized_user_success(authorized_api_client, task_data) -> None:
    # Create a task
    client, auth_user = authorized_api_client
    response_create = client.post("/api/tasks/", data=task_data, format="json")
    response_create_data = response_create.json()
    assert response_create.status_code == 201
    assert response_create_data.get("title") == task_data["title"]
    assert response_create_data.get("owner") == auth_user.id

    # Read the task
    response_create_data = response_create.json()
    response_read = client.get(f"/api/tasks/{response_create_data.get('id')}/", format="json")
    assert response_read.status_code == 200
    assert response_read.json().get("title") == task_data["title"]


@pytest.mark.django_db
def test_view_tasks_by_unauthorized_user_success(api_client, task_without_owner, task_with_owner) -> None:
    response_read = api_client.get(f"/api/tasks/", format="json")
    assert response_read.status_code == 200
    assert len(response_read.json()) == 1
    assert response_read.json()[0].get('owner') is None


@pytest.mark.django_db
def test_view_tasks_by_authorized_user_success(authorized_api_client, task_without_owner, task_with_owner) -> None:
    client, auth_user = authorized_api_client
    response_read = client.get(f"/api/tasks/", format="json")
    assert response_read.status_code == 200
    assert len(response_read.json()) == 2

    task_owners_data = [task.get('owner') for task in response_read.json()]
    assert None in task_owners_data
    assert auth_user.id in task_owners_data
    assert len(task_owners_data) == 2


@pytest.mark.django_db
def test_read_owners_task_by_unauthorized_user_fail(api_client, task_with_owner) -> None:
    response_read = api_client.get(f"/api/tasks/{task_with_owner.id}/", format="json")
    assert response_read.status_code == 404


@pytest.mark.django_db
def test_filter_tasks_by_done_status_unauthorized_user_success(
        api_client, tasks_without_owner_with_different_statuses) -> None:
    response_read = api_client.get(f"/api/tasks/?is_done=1", format="json")
    assert response_read.status_code == 200
    assert len(response_read.json()) == 1
    assert response_read.json()[0].get('is_done') is True


@pytest.mark.django_db
def test_filter_tasks_by_status_unauthorized_user_success(
        api_client, tasks_without_owner_with_different_statuses) -> None:
    response_read = api_client.get(f"/api/tasks/?is_done=0", format="json")
    assert response_read.status_code == 200
    assert len(response_read.json()) == 1
    assert response_read.json()[0].get('is_done') is False


@pytest.mark.django_db
def test_search_tasks_unauthorized_user_success(
        api_client, task_without_owner, task_data) -> None:
    response_read = api_client.get(f"/api/tasks/?search=Doctor", format="json")
    assert response_read.status_code == 200
    assert len(response_read.json()) == 1
    assert 'Doctor' in response_read.json()[0].get('title')


@pytest.mark.django_db
def test_order_tasks_unauthorized_user_success(
        api_client, tasks_without_owner_different_in_time, task_data) -> None:
    task1, task2 = tasks_without_owner_different_in_time
    response_read = api_client.get(f"/api/tasks/?ordering=-created_at", format="json")
    assert response_read.status_code == 200
    assert len(response_read.json()) == 2
    assert response_read.json()[0].get('id') == task2.id
    assert response_read.json()[1].get('id') == task1.id


@pytest.mark.django_db
def test_update_task_by_unauthorized_user_success(api_client, task_without_owner, task_data) -> None:
    task_data["title"] = "Cancel Doctor Appointment"
    response_update = api_client.put(
        f"/api/tasks/{task_without_owner.id}/", data=task_data, format="json"
    )
    response_update_data = response_update.json()
    assert response_update.status_code == 200
    assert response_update_data.get('title') == task_data["title"]
    assert response_update_data.get('title') != task_without_owner.title


@pytest.mark.django_db
def test_update_not_existing_task_by_unauthorized_user_fail(api_client, task_without_owner, task_data) -> None:
    task_data["title"] = "Cancel Doctor Appointment"
    response_update = api_client.put(
        f"/api/tasks/{task_without_owner.id}1000/", data=task_data, format="json"
    )
    assert response_update.status_code == 404


@pytest.mark.django_db
def test_update_other_owner_tasks_by_authorized_user_fail(
        authorized_api_client, task_with_different_owner, task_data) -> None:
    task, new_user = task_with_different_owner
    client, user = authorized_api_client

    task_data["title"] = "Cancel Doctor Appointment"
    response_update = client.put(
        f"/api/tasks/{task.id}/", data=task_data, format="json"
    )
    assert response_update.status_code == 404


@pytest.mark.django_db
def test_delete_task_by_unauthorized_user_success(api_client, task_without_owner) -> None:
    response_delete = api_client.delete(f"/api/tasks/{task_without_owner.id}/", format="json")
    assert response_delete.status_code == 204

    response_read = api_client.get(f"/api/tasks/{task_without_owner.id}/", format="json")
    assert response_read.status_code == 404


@pytest.mark.django_db
def test_delete_other_owner_task_by_unauthorized_user_fail(api_client, task_with_owner) -> None:
    response_delete = api_client.delete(f"/api/tasks/{task_with_owner.id}/", format="json")
    assert response_delete.status_code == 404
