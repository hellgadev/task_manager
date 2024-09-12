import time
from typing import Tuple

import pytest
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from apps.tasks.models import Task


@pytest.fixture
def task_data() -> dict:
    return {
        'title': 'Schedule Doctor Appointment',
        'description': 'Book a routine check-up with your primary care physician.'
    }


@pytest.fixture
def user_login_data() -> dict:
    return {
        'username': 'someone',
        'password': 'password'
    }


@pytest.fixture
def user(db, django_user_model, user_login_data) -> User:
    return django_user_model.objects.create_user(**user_login_data)


@pytest.fixture(scope="function")
def api_client() -> APIClient:
    """
    Fixture to provide an API client
    :return: APIClient
    """
    yield APIClient()


@pytest.fixture
def authorized_api_client(user: User) -> Tuple[APIClient, User]:
    client = APIClient()
    token, _ = Token.objects.get_or_create(user=user)
    client.force_authenticate(user=user, token=token)
    return client, user


@pytest.fixture
def task_without_owner(db, task_data) -> Task:
    return Task.objects.create(**task_data)


@pytest.fixture
def task_with_owner(user, task_data) -> Task:
    return Task.objects.create(**task_data, owner=user)


@pytest.fixture
def task_with_different_owner(db, django_user_model) -> Tuple[Task, User]:
    new_user = django_user_model.objects.create_user(username="James", password="mybestpassword")
    task = Task.objects.create(title="Renew Passport", owner=new_user)
    return task, new_user


@pytest.fixture
def tasks_without_owner_with_different_statuses(db, task_data) -> Tuple[Task, Task]:
    task = Task.objects.create(**task_data)
    done_task = Task.objects.create(**task_data, is_done=True)
    return task, done_task


@pytest.fixture
def tasks_without_owner_different_in_time(db, task_data) -> Tuple[Task, Task]:
    task1 = Task.objects.create(**task_data)
    time.sleep(1)
    task2 = Task.objects.create(**task_data, is_done=True)
    return task1, task2
