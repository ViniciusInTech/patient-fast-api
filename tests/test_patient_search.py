import pytest
from fastapi import HTTPException
from src.models.patient import PatientCreate
from src.services.patient_add import create_patient
from src.services.patient_search import get_patients, get_patient_by_id
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


def test_get_patients_by_name(db):
    patient_data_1 = PatientCreate(
        name="Arya Stark",
        birth_date=date(2000, 5, 1),
        health_conditions="Healthy",
        gender="Feminine",
        address="Winterfell"
    )
    patient_data_2 = PatientCreate(
        name="Jon Snow",
        birth_date=date(1990, 6, 12),
        health_conditions="Healthy",
        gender="Masculine",
        address="Beyond the Wall"
    )

    create_patient(patient_data_1)
    create_patient(patient_data_2)

    patients = get_patients(name="Arya")

    assert len(patients) == 1
    assert patients[0].name == "Arya Stark"


def test_get_patients_by_health_condition(db):
    patient_data_1 = PatientCreate(
        name="Daenerys Targaryen",
        birth_date=date(1985, 12, 1),
        health_conditions="Healthy",
        gender="Feminine",
        address="Dragonstone"
    )
    patient_data_2 = PatientCreate(
        name="Tyrion Lannister",
        birth_date=date(1970, 6, 22),
        health_conditions="Alcoholism",
        gender="Masculine",
        address="Casterly Rock"
    )

    create_patient(patient_data_1)
    create_patient(patient_data_2)

    patients = get_patients(health_conditions="Alcoholism")

    assert len(patients) == 1
    assert patients[0].name == "Tyrion Lannister"


def test_get_patient_by_id(db):
    patient_data = PatientCreate(
        name="Cersei Lannister",
        birth_date=date(1970, 5, 5),
        health_conditions="Healthy",
        gender="Feminine",
        address="King's Landing"
    )

    created_patient = create_patient(patient_data)

    patient = get_patient_by_id(created_patient.id)

    assert patient.name == "Cersei Lannister"
    assert patient.id == created_patient.id


def test_get_patient_by_id_not_found(db):
    with pytest.raises(HTTPException) as exc_info:
        get_patient_by_id(999)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Patient with ID 999 not found."


def test_get_patients_no_results(db):

    patients = get_patients(name="Nonexistent Name")

    assert len(patients) == 0
