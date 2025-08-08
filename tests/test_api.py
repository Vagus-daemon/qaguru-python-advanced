import pytest
import requests
from http import HTTPStatus
from math import ceil
from models.User import User


@pytest.fixture
def users(app_url):
    response = requests.get(f"{app_url}/api/users/")
    assert response.status_code == HTTPStatus.OK
    return response.json()


def test_users_no_duplicates(users):
    users_ids = [user["id"] for user in users['items']]
    assert len(users_ids) == len(set(users_ids)), f"Обнаружены дубликаты: {users_ids.remove(set(users_ids))}"


def test_users_validation(users):
    for user in users['items']:
        assert User.model_validate(user), f"Пользователь {user} не соответствует структуре модели User"


@pytest.mark.parametrize("user_id", [num for num in range(1, 13)])
def test_user(app_url, user_id):
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


@pytest.mark.parametrize("page, size",
                         [(1, 1), (12, 1), (1, 3), (2, 3), (1, 15), (2, 15),
                          (1, 10), (2, 10), (2, 4), (4, 4), (3, 5), (4, 5)])
def test_pagination(app_url, page, size, users):
    total = users['total']

    response = requests.get(f"{app_url}/api/users/?page={page}&size={size}")
    assert response.status_code == HTTPStatus.OK

    response = response.json()
    response_user = response['items']
    total_pages = ceil(total / size)
    last_page = total % size
    per_page = size % total
    current_lenght = last_page if page == total_pages and last_page != 0 else size

    assert response["total"] == total, "Некорректный total в ответе"
    assert response['page'] == page, "Некорректный page в ответе"
    assert response['size'] == size, "Некорректный size в ответе"
    assert response['pages'] == total_pages, "Некорректный total_pages в ответе"
    if page <= total_pages:
        start_id = (page - 1) * per_page
        x = users['items'][start_id: start_id + current_lenght]
        assert len(response_user) == current_lenght, \
            f"Количество пользователей в ответе = {len(response_user)}, должно быть  {current_lenght}"
        assert response_user == x, "Cписок пользователей не верен"
    else:
        assert len(response_user) == 0, "Список пользователей в ответе должен быть пустым"
