import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi import HTTPException
from src.models.user import Base
from src.services.auth import verify_password
from src.services.user_service import create_user, authenticate_user


@pytest.fixture(scope="module")
def test_db():
    engine = create_engine("sqlite:///:memory:")
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def test_create_user(test_db):
    username = "JonSnow"
    password = "WinterIsComing123"

    user = create_user(test_db, username, password)

    assert user.username == "JonSnow"
    assert verify_password(password, user.hashed_password)


def test_authenticate_user_success(test_db):
    username = "AryaStark"
    password = "NotToday123"

    create_user(test_db, username, password)

    token = authenticate_user(test_db, username, password)

    assert isinstance(token, str)
    assert len(token) > 0


def test_authenticate_user_invalid_password(test_db):
    username = "TyrionLannister"
    password = "IDrinkAndIKnowThings"

    create_user(test_db, username, password)

    with pytest.raises(HTTPException) as excinfo:
        authenticate_user(test_db, username, "WrongPassword123")

    assert excinfo.value.status_code == 401
    assert excinfo.value.detail == "Credenciais inválidas"


def test_authenticate_user_nonexistent_user(test_db):
    username = "DaenerysTargaryen"
    password = "Dracarys123"

    with pytest.raises(HTTPException) as excinfo:
        authenticate_user(test_db, username, password)

    assert excinfo.value.status_code == 401
    assert excinfo.value.detail == "Credenciais inválidas"
