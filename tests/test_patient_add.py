import pytest
from datetime import date
from src.models.patient import PatientCreate
from src.services.patient_add import create_patient
from src.config.database import SessionLocal, engine, Base
from fastapi import HTTPException


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


def test_create_patient_successful(db):
    patient_data = PatientCreate(
        name="Jon Snow",
        birth_date=date(1990, 5, 15),
        health_conditions="cancer",
        gender="Masculine",
        address="Winterfell, North"
    )

    created_patient = create_patient(patient_data)

    assert created_patient.name == "Jon Snow"
    assert created_patient.birth_date == date(1990, 5, 15)
    assert created_patient.id is not None


def test_create_patient_with_future_birth_date(db):
    future_patient_data = PatientCreate(
        name="Daenerys Targaryen",
        birth_date=date(2025, 1, 1),
        health_conditions="Test condition",
        gender="Feminine",
        address="Dragonstone, Narrow Sea"
    )

    with pytest.raises(HTTPException) as exc_info:
        create_patient(future_patient_data)

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "The date of birth cannot be a future date."


def test_create_patient_with_name_null(db):
    patient_null_name = PatientCreate(
        name="",
        birth_date=date(2000, 1, 1),
        health_conditions="Test condition",
        gender="Feminine",
        address="Dragonstone, Narrow Sea"
    )
    with pytest.raises(HTTPException) as exc_info:
        create_patient(patient_null_name)

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "The name must contain at least two words."


def test_database_session_management(db):
    patient_data = PatientCreate(
        name="Arya Stark",
        birth_date=date(2000, 3, 10),
        health_conditions="Stealthy and healthy",
        gender="Feminine",
        address="Braavos"
    )

    created_patient = create_patient(patient_data)

    assert created_patient.name == patient_data.name


def test_multiple_patient_creation(db):
    patients_data = [
        PatientCreate(
            name="Tyrion Lannister",
            birth_date=date(1985, 6, 15),
            health_conditions="Smart and quick-witted",
            gender="Masculine",
            address="Casterly Rock"
        ),
        PatientCreate(
            name="Cersei Lannister",
            birth_date=date(1990, 8, 20),
            health_conditions="Scheming and ambitious",
            gender="Feminine",
            address="King's Landing"
        )
    ]

    created_patients = [create_patient(patient) for patient in patients_data]

    assert len(created_patients) == 2
    assert created_patients[0].name == "Tyrion Lannister"
    assert created_patients[1].name == "Cersei Lannister"
