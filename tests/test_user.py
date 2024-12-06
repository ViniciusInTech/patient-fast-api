import pytest
from pydantic import ValidationError
from src.schemas.user import UserCreate, UserLogin


def test_user_login_valid():
    user_data = {
        "username": "JonSnow",
        "password": "WinterIsComing123"
    }

    user = UserLogin(**user_data)

    assert user.username == "JonSnow"
    assert user.password == "WinterIsComing123"


def test_user_login_invalid_missing_field():
    user_data = {
        "username": "JonSnow"
    }

    with pytest.raises(ValidationError) as excinfo:
        UserLogin(**user_data)

    assert "password" in str(excinfo.value)


def test_user_create_valid():
    user_data = {
        "username": "AryaStark",
        "password": "NotToday123"
    }

    user = UserCreate(**user_data)

    assert user.username == "AryaStark"
    assert user.password == "NotToday123"

