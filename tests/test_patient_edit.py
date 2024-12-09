import pytest
from fastapi import HTTPException
from src.models.patient import PatientCreate
from src.services.patient_add import create_patient
from src.services.patient_edit import update_patient
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


def test_update_patient_successful(db):
    patient_data = PatientCreate(
        name="Tyrion Lannister",
        birth_date=date(1970, 6, 22),
        health_conditions="Healthy",
        gender="Masculine",
        address="Casterly Rock"
    )

    created_patient = create_patient(patient_data)

    updated_patient_data = PatientCreate(
        name="Tyrion Lannister Updated",
        birth_date=date(1970, 6, 22),
        health_conditions="No conditions",
        gender="Masculine",
        address="Updated Address"
    )

    updated_patient = update_patient(created_patient.id, updated_patient_data)

    assert updated_patient.name == "Tyrion Lannister Updated"
    assert updated_patient.health_conditions == "No conditions"
    assert updated_patient.address == "Updated Address"


def test_update_patient_not_found(db):
    with pytest.raises(HTTPException) as exc_info:
        update_patient(999, PatientCreate(
            name="Nonexistent Patient",
            birth_date=date(1990, 5, 15),
            health_conditions="No conditions",
            gender="Masculine",
            address="Nonexistent Address"
        ))

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Patient not found with ID 999. "


def test_update_patient_invalid_data(db):
    patient_data = PatientCreate(
        name="Jaime Lannister",
        birth_date=date(1985, 6, 15),
        health_conditions="Healthy",
        gender="Masculine",
        address="Casterly Rock"
    )

    created_patient = create_patient(patient_data)

    invalid_data = PatientCreate(
        name="Jaime",
        birth_date=date(1985, 6, 15),
        health_conditions="Healthy",
        gender="Masculine",
        address="Casterly Rock"
    )

    with pytest.raises(HTTPException) as exc_info:
        update_patient(created_patient.id, invalid_data)

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "The name must contain at least two words."
