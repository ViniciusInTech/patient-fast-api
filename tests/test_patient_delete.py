import pytest
from fastapi import HTTPException
from src.models.patient import PatientCreate
from src.services.patient_add import create_patient
from src.services.patient_delete import delete_patient
from src.config.database import SessionLocal, engine, Base
from datetime import date


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


def test_delete_patient_successful(db):
    patient_data = PatientCreate(
        name="Jaime Lannister",
        birth_date=date(1985, 6, 15),
        health_conditions="Healthy",
        gender="Masculine",
        address="Casterly Rock"
    )

    created_patient = create_patient(patient_data)

    response = delete_patient(created_patient.id)

    assert response["detail"] == "Patient deleted successfully."


def test_delete_patient_not_found(db):
    with pytest.raises(HTTPException) as exc_info:
        delete_patient(999)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Patient not found."
