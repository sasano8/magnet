import pytest
import asyncio
from . import client
import main
from magnet import logger


def test_view_guest_create_login_delete():
    USERNAME = "mytest@test.com"
    PASSWORD = "85293nucAZ52347"
    correct_data = {
        "id": None,
        "email": "mytest@test.com",
        "username": "mytest@test.com",
        "full_name": None,
        "disabled": False,
        "is_active": True,
        "items": []
    }

    response = client.post(
        url="/users/guest",
        json=dict(
            email=USERNAME,
            password=PASSWORD
        )
    )
    data = response.json()
    correct_data["id"] = data["id"]
    assert data == correct_data
    assert response.status_code == 200

    # login
    # If you need to send Form Data instead of JSON, use the data parameter instead.
    response = client.post(
        url="/users/guest/login",
        data=dict(
            grant_type="password",
            username=USERNAME,
            password=PASSWORD,
            scope=" ".join(["me", "items"]),  # 複数のスコープは、スペースで区切って指定する
            client_id=None,
            client_secret=None
        )
    )
    assert response.status_code == 200
    data = response.json()
    assert data["access_token"]
    assert data["token_type"] == "bearer"
    access_token = data["access_token"]

    response = client.get(
        headers={"Authorization": f"Bearer {access_token}"},
        url="/users/me"
    )
    assert response.status_code == 200
    data = response.json()
    assert data == correct_data

