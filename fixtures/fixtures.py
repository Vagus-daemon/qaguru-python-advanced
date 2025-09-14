import pytest
from config import Server
from utils.base_session import BaseSession


@pytest.fixture(scope='session')
def base_session(env):
    with BaseSession(base_url=Server(env).reqres) as session:
        yield session
