import pytest
from faker import Faker
from http import HTTPStatus
from app.database.users import get_user

fake = Faker()


def test_users_no_duplicates(helper):
    users_ids = [user["email"] for user in helper.get_all_users().json()]
    assert len(users_ids) == len(set(users_ids)), f"Обнаружены дубликаты: {users_ids.remove(set(users_ids))}"


@pytest.mark.parametrize("user_id", [13])
def test_user_nonexistent_values(helper, user_id):
    response = helper.get_one_user(user_id=user_id)
    assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.parametrize("user_id", [-1, 0, 'string'])
def test_user_invalid_values(helper, user_id):
    response = helper.get_one_user(user_id=user_id)
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_create_user(helper):
    data = {
        "email": f"{fake.email()}",
        "first_name": f"{fake.first_name()}",
        "last_name": f"{fake.last_name()}",
        "avatar": "https://example.com/avatar.jpg",
    }

    create_response = helper.create_new_user(
        email=data["email"],
        first_name=data["first_name"],
        last_name=data["last_name"],
        avatar=data["avatar"]
    )
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
    delete_response = helper.delete_one_user(user_id=new_user_id)
    assert delete_response.status_code == HTTPStatus.OK


def test_delete_user(helper):
    get_users_response = helper.get_all_users()
    data = {
        "email": f"{fake.email()}",
        "first_name": f"{fake.first_name()}",
        "last_name": f"{fake.last_name()}",
        "avatar": "https://example.com/avatar.jpg",
    }

    create_response = helper.create_new_user(
        email=data["email"],
        first_name=data["first_name"],
        last_name=data["last_name"],
        avatar=data["avatar"]
    )
    assert create_response.status_code == HTTPStatus.CREATED

    created_user = create_response.json()
    new_user_id = created_user['id']
    delete_response = helper.delete_one_user(user_id=new_user_id)
    assert delete_response.status_code == HTTPStatus.OK

    user = helper.get_one_user(user_id=new_user_id)
    assert user.status_code == HTTPStatus.NOT_FOUND

    get_users_response_after_del = helper.get_all_users()
    assert len(get_users_response.json()) == len(get_users_response_after_del.json())


def test_update_user(helper):
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
    create_response = helper.create_new_user(
        email=data["email"],
        first_name=data["first_name"],
        last_name=data["last_name"],
        avatar=data["avatar"]
    )
    assert create_response.status_code == HTTPStatus.CREATED
    created_user = create_response.json()
    new_user_id = created_user['id']

    update_response = helper.update_user_data(
        user_id=new_user_id,
        email=updated_data["email"],
        first_name=updated_data["first_name"],
        last_name=updated_data["last_name"],
        avatar=data["avatar"]
    )
    assert update_response.status_code == HTTPStatus.OK
    updated_user = update_response.json()
    assert updated_user['email'] != created_user['email']
    assert updated_user['first_name'] != created_user['first_name']
    assert updated_user['last_name'] != created_user['last_name']

    delete_response = helper.delete_one_user(user_id=new_user_id)
    assert delete_response.status_code == HTTPStatus.OK
