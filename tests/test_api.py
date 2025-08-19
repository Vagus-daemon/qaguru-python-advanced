import pytest
import requests
from http import HTTPStatus
from app.models.User import User
from app.database.users import get_user
from faker import Faker

fake = Faker()





@pytest.fixture
def users(app_url):
    response = requests.get(f"{app_url}/api/users/")
    assert response.status_code == HTTPStatus.OK
    return response.json()


def test_users_no_duplicates(users):
    users_ids = [user["email"] for user in users]
    assert len(users_ids) == len(set(users_ids)), f"Обнаружены дубликаты: {users_ids.remove(set(users_ids))}"


@pytest.mark.usefixtures("fill_test_data")
def test_users_validation(users):
    for user in users:
        assert User.model_validate(user), f"Пользователь {user} не соответствует структуре модели User"


def test_user(app_url, fill_test_data):
    for user_id in (fill_test_data[0], fill_test_data[-1]):
        response = requests.get(f"{app_url}/api/users/{user_id}")
        assert response.status_code == HTTPStatus.OK
        user = response.json()
        User.model_validate(user)


@pytest.mark.parametrize("user_id", [13])
def test_user_nonexistent_values(app_url, user_id):
    response = requests.get(f"{app_url}/api/users/{user_id}")
    assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.parametrize("user_id", [-1, 0, 'string'])
def test_user_invalid_values(app_url, user_id):
    response = requests.get(f"{app_url}/api/users/{user_id}")
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_create_user(app_url):
    data = {
        "email": f"{fake.email()}",
        "first_name": f"{fake.first_name()}",
        "last_name": f"{fake.last_name()}",
        "avatar": "https://example.com/avatar.jpg",
    }

    create_response = requests.post(f"{app_url}/api/users/", json=data)
    assert create_response.status_code == HTTPStatus.CREATED

    created_user = create_response.json()
    assert created_user["email"] == data["email"]
    assert created_user["first_name"] == data["first_name"]
    assert created_user["last_name"] == data["last_name"]

    user_from_db = get_user(created_user["id"])
    assert user_from_db is not None
    assert user_from_db.email == data["email"]
    assert user_from_db.first_name == data["first_name"]
    assert user_from_db.last_name == data["last_name"]
    new_user_id = created_user['id']
    delete_response = requests.delete(f"{app_url}/api/users/{new_user_id}")
    assert delete_response.status_code == HTTPStatus.OK


def test_delete_user(app_url):
    get_users_response = requests.get(f"{app_url}/api/users/")
    data = {
        "email": f"{fake.email()}",
        "first_name": f"{fake.first_name()}",
        "last_name": f"{fake.last_name()}",
        "avatar": "https://example.com/avatar.jpg",
    }

    create_response = requests.post(f"{app_url}/api/users/", json=data)
    assert create_response.status_code == HTTPStatus.CREATED

    created_user = create_response.json()
    new_user_id = created_user['id']
    delete_response = requests.delete(f"{app_url}/api/users/{new_user_id}")
    assert delete_response.status_code == HTTPStatus.OK

    user = requests.get(f"{app_url}/api/users/{new_user_id}")
    assert user.status_code == HTTPStatus.NOT_FOUND

    get_users_response_after_del = requests.get(f"{app_url}/api/users/")
    assert len(get_users_response.json()) == len(get_users_response_after_del.json())


def test_update_user(app_url):
    data = {
        "email": f"{fake.email()}",
        "first_name": f"{fake.first_name()}",
        "last_name": f"{fake.last_name()}",
        "avatar": "https://example.com/avatar.jpg",
    }
    updated_data = {
        "email": f"{fake.email()}",
        "first_name": f"{fake.first_name()}",
        "last_name": f"{fake.last_name()}",
    }
    create_response = requests.post(f"{app_url}/api/users/", json=data)
    assert create_response.status_code == HTTPStatus.CREATED
    created_user = create_response.json()
    new_user_id = created_user['id']

    update_response = requests.patch(f"{app_url}/api/users/{new_user_id}", json=updated_data)
    assert update_response.status_code == HTTPStatus.OK
    updated_user = update_response.json()
    assert updated_user['email'] != created_user['email']
    assert updated_user['first_name'] != created_user['first_name']
    assert updated_user['last_name'] != created_user['last_name']

    delete_response = requests.delete(f"{app_url}/api/users/{new_user_id}")
    assert delete_response.status_code == HTTPStatus.OK

