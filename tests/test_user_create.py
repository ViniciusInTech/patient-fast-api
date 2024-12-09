import pytest
from fastapi import HTTPException
from src.schemas.user import User
from src.services.auth import hash_password
from src.config.database import SessionLocal, engine, Base
from src.services.user_create import create_user


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
def existing_user(db):
    user = User(username="existing_user", hashed_password=hash_password("password"))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def test_create_user_successful(db):
    username = "new_user"
    password = "password123"

    new_user = create_user(username, password)

    assert new_user.username == username
    assert new_user.hashed_password is not None
    assert isinstance(new_user.hashed_password, str)


def test_create_user_with_existing_username(db, existing_user):
    username = "existing_user"
    password = "newpassword123"

    with pytest.raises(HTTPException) as exc_info:
        create_user(username, password)

    assert exc_info.value.status_code == 409
    assert exc_info.value.detail == "The username is already in use."


