import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi import HTTPException
from datetime import date
from src.models.patient import Patient, Base
from src.schemas.patient import PatientCreate
from src.services.patient_edit import update_patient


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


def test_update_existing_patient(test_db):
    patient = Patient(
        name="Jon Snow",
        birth_date=date(1990, 1, 1),
        health_conditions="Night Watch Trauma",
        gender="Male",
        address="Castle Black",
    )
    test_db.add(patient)
    test_db.commit()

    updated_data = PatientCreate(
        name="Jon Stark",
        birth_date=date(1990, 1, 1),
        health_conditions="Recovered from Night Watch Trauma",
        gender="Male",
        address="Winterfell",
    )
    updated_patient = update_patient(test_db, patient.id, updated_data)

    assert updated_patient.name == "Jon Stark"
    assert updated_patient.birth_date == date(1990, 1, 1)
    assert updated_patient.health_conditions == "Recovered from Night Watch Trauma"
    assert updated_patient.gender == "Male"
    assert updated_patient.address == "Winterfell"


def test_update_nonexistent_patient(test_db):
    updated_data = PatientCreate(
        name="Cersei Lannister",
        birth_date=date(1980, 5, 5),
        health_conditions="Excessive wine consumption",
        gender="Female",
        address="Red Keep",
    )

    nonexistent_id = 9999
    with pytest.raises(HTTPException) as excinfo:
        update_patient(test_db, nonexistent_id, updated_data)

    assert excinfo.value.status_code == 404
    assert excinfo.value.detail == f"Patient not found with ID {nonexistent_id}. "
