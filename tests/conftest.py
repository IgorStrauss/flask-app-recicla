import pytest
from app import create_app
from app.models import User


@pytest.fixture(scope="module")
def app():
    return create_app()


@pytest.fixture(scope="module")
def new_user():
    return User('1' 'Peter', 'Parker', 'spider@icloud.com', 'senha')
