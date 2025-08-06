import requests

#url = "https://reqres.in/api/"
headers = {'x-api-key': 'reqres-free-v1'}

url = "http://localhost:8000/api/"


def test_id_email_from_request_returns_in_response():
    expected_id = 2
    expected_email = "janet.weaver@reqres.in"
    response = requests.get(url + f'users/{expected_id}')
    body = response.json()
    assert response.status_code == 200
    assert body["id"] == expected_id
    assert body["email"] == expected_email


def test_get_users_returns_unique_users():
    response = requests.get(url=url + 'users', params={"page": 2, "per_page": 4}, verify=False, headers=headers)
    body = response.json()
    actual_data = body["data"]
    ids = [element["id"] for element in actual_data]
    assert len(ids) == len(set(ids))


def test_login_user():
    data = {"email": "charles.morris@reqres.in", "password": "qwerty"}
    response = requests.post(url=url + 'login', headers=headers, json=data)
    expected_token = 'QpwL5tke4Pnpja7X5'
    body = response.json()
    assert response.status_code == 200
    assert body['token'] == expected_token


def test_user_registration():
    data = {"email": "charles.morris@reqres.in", "password": "qwerty"}
    response = requests.post(url=url + 'register', headers=headers, data=data)
    expected_token = 'QpwL5tke4Pnpja7X5'
    body = response.json()
    assert response.status_code == 200
    assert body['token'] == expected_token

