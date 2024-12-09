import os
import pytest
from jose import jwt
from fastapi import HTTPException
from src.services.auth import (
    hash_password,
    verify_password,
    create_access_token,
    decode_access_token,
    validate_user,
    get_env_var
)

SECRET_KEY = "my_test_secret_key"
os.environ["SECRET_KEY"] = SECRET_KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def test_get_env_var():
    assert get_env_var("SECRET_KEY") == SECRET_KEY

    with pytest.raises(RuntimeError):
        get_env_var("NON_EXISTENT_VAR")


def test_hash_password():
    password = "WinterIsComing123"
    hashed_password = hash_password(password)

    assert hashed_password != password
    assert verify_password(password, hashed_password)


def test_verify_password_invalid():
    password = "WinterIsComing123"
    hashed_password = hash_password(password)

    assert not verify_password("WrongPassword", hashed_password)


def test_decode_access_token():
    data = {"sub": "daenerys.targaryen"}
    token = create_access_token(data)
    decoded_data = decode_access_token(token)

    assert decoded_data["sub"] == "daenerys.targaryen"


def test_decode_access_token_invalid():
    invalid_token = "invalid_token_string"
    decoded_data = decode_access_token(invalid_token)

    assert decoded_data is None


def test_validate_user():
    data = {"sub": "tyrion.lannister"}
    token = create_access_token(data)
    user = validate_user(token)

    assert user == "tyrion.lannister"


def test_validate_user_invalid_token():
    invalid_token = "invalid_token_string"

    with pytest.raises(HTTPException) as excinfo:
        validate_user(invalid_token)

    assert excinfo.value.status_code == 401
    assert excinfo.value.detail == "Invalid or expired token."


def test_validate_user_missing_sub():
    token = jwt.encode({}, SECRET_KEY, algorithm=ALGORITHM)

    with pytest.raises(HTTPException) as excinfo:
        validate_user(token)

    assert excinfo.value.status_code == 401
    assert excinfo.value.detail == "Invalid or expired token."
