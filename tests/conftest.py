import pytest
from fixtures.helper import Helper
from config import Server


def pytest_addoption(parser):
    parser.addoption("--env", default="dev")


@pytest.fixture(scope="session")
def env(request):
    return request.config.getoption("--env")


@pytest.fixture(scope="session")
def helper(env) -> Helper:
    return Helper(host=Server(env).reqres)
