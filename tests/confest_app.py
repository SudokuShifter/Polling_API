from datetime import datetime, timedelta

import pytest
from fastapi.testclient import TestClient
from main import app
from schemas.user import UserIn
from faker import Faker
from routers.JWT.JWT_token import JWTToken

fake = Faker()


@pytest.fixture
def client():
    client = TestClient(app)
    return client


@pytest.fixture
def current_user():
    data = {'username': 'string', 'password': 'string'}
    return data

@pytest.fixture
def incorrect_user():
    data = {'username': 'string', 'password': '1232233'}
    return data

@pytest.fixture
def new_user_for_register():
    data = {
        'username': str(fake.user_name()),
        'email': str(fake.email()),
        'password': str(fake.password()),
        'admin_token': '123123'}
    return data

@pytest.fixture
def user_data_for_update():
    data = {
        'username': str(fake.user_name()),
        'email': str(fake.email())
    }
    return data

@pytest.fixture
def exist_poll():
    response_data = {'data': {'poll': "{'poll': ['Poll_title - string', 'Poll_id - 2']}",
                              'questions': "{'questions': []}"}, 'detail': None, 'success': True}
    return response_data

@pytest.fixture
def auth_token():
    payload = {
        'sub': {
            'username': 'string',
            'id': 1,
            'role': 'USER'
        }
    }
    token = JWTToken.generate_token(payload)
    return token

@pytest.fixture
def new_poll():
    data = {'title': 'abobasss'}
    return data