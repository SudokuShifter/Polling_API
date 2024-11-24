import pytest
from fastapi import Response
from schemas.user import UserIn
from routers.JWT.JWT_token import JWTToken


from .confest_app import (
    client,
    current_user,
    incorrect_user,
    new_user_for_register,
    user_data_for_update,
    exist_poll,
    auth_token,
    new_poll)


def test_login_route(client, current_user):
    data = current_user
    response = client.post("user/login", data=data)
    assert response.status_code == 200
    assert response.json()['message'] == 'Successfully logged in as string'


def test_logout_route_error(client, incorrect_user):
    incorrect_data = incorrect_user
    response = client.post("user/login", data=incorrect_data)
    assert response.status_code == 401


def test_register_route(client, new_user_for_register):
    data = new_user_for_register
    response = client.post("user/register", user=data)
    assert response.status_code == 200


def test_get_all_polls(client):
    response = client.get("/polls/get_polls")
    assert response.status_code == 200
    assert response.json()['success'] == True


def test_get_poll_by_id(client, exist_poll):
    response = client.get("/polls/get_poll/2")
    assert response.status_code == 200
    assert response.json() == exist_poll

def test_create_poll(client):
    response = client.post("/polls/create_poll", data={'title': 'test'})
    assert response.status_code == 401

def test_update_poll(client):
    response = client.put("/polls/update_poll/2", data={'title': 'test'})
    assert response.status_code == 401

def test_delete_poll(client):
    response = client.delete("/polls/delete_poll/2")
    assert response.status_code == 401

def test_add_question(client):
    response = client.post("/polls/add_question/2", data={'title': 'test'})
    assert response.status_code == 401

def test_remove_question(client):
    response = client.delete("/polls/remove_question/2/1")
    assert response.status_code == 401

def test_get_results(client):
    response = client.get("/answer/my_results")
    assert response.status_code == 401

