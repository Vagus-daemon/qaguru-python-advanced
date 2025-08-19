import requests
from http import HTTPStatus


def test_service(app_url):
    response = requests.get(f"{app_url}/status/")
    body = response.json()
    print(response.json())
    assert response.status_code == HTTPStatus.OK
    assert body['database'] is True
