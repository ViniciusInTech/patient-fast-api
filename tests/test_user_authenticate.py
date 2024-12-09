import pytest
from fastapi import HTTPException
from src.schemas.user import User
from src.services.auth import verify_password, create_access_token, hash_password
from src.config.database import SessionLocal, engine, Base
from src.services.user_authenticate import authenticate_user


def setup_module(module):
    Base.metadata.create_all(bind=engine)


def teardown_module(module):
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db():
    connection = engine.connect()
    transaction = connection.begin()
    session = SessionLocal()

    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()


@pytest.fixture
def user_data(db):
    hashed_password = hash_password("user_password")
    user = User(
        username="testuser",
        hashed_password=hashed_password
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def test_authenticate_user_successful(db, user_data):
    token = authenticate_user(user_data.username, "user_password")

    assert token is not None
    assert isinstance(token, str)


def test_authenticate_user_invalid_username(db):
    with pytest.raises(HTTPException) as exc_info:
        authenticate_user("invaliduser", "user_password")

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Invalid credentials"


def test_authenticate_user_empty_username(db):
    with pytest.raises(HTTPException) as exc_info:
        authenticate_user("", "user_password")

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Invalid credentials"


