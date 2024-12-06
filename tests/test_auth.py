import pytest
from datetime import datetime, timedelta

from jose import jwt

from src.services.auth import (
    hash_password,
    verify_password,
    create_access_token,
    decode_access_token,
    validate_user,
    SECRET_KEY,
    ALGORITHM,
)


def test_hash_and_verify_password():
    plain_password = "minhasenhamuitoforte"
    hashed_password = hash_password(plain_password)

    assert plain_password != hashed_password

    assert verify_password(plain_password, hashed_password)

    assert not verify_password("minhasenha123", hashed_password)


def test_create_and_decode_access_token():

    data = {"sub": "testuser"}
    token = create_access_token(data)

    assert isinstance(token, str) and len(token) > 0

    decoded_data = decode_access_token(token)
    assert decoded_data is not None
    assert decoded_data["sub"] == "testuser"

    assert "exp" in decoded_data

    invalid_token = token + "salsal"
    assert decode_access_token(invalid_token) is None


def test_validate_user():
    valid_data = {"sub": "validuser"}
    valid_token = create_access_token(valid_data)

    user = validate_user(valid_token)
    assert user == "validuser"

    invalid_token = valid_token + "invalid"
    with pytest.raises(Exception) as excinfo:
        validate_user(invalid_token)
    assert "Invalid or expired token." in str(excinfo.value)

    expired_data = {"sub": "expireduser", "exp": datetime.utcnow() - timedelta(minutes=1)}
    expired_token = jwt.encode(expired_data, SECRET_KEY, algorithm=ALGORITHM)
    with pytest.raises(Exception) as excinfo:
        validate_user(expired_token)
    assert "Invalid or expired token." in str(excinfo.value)
