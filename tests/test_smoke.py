from http import HTTPStatus


def test_service(helper):
    response = helper.get_app_status()
    body = response.json()
    assert response.status_code == HTTPStatus.OK
    assert body['database'] is True
