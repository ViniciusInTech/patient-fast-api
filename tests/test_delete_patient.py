import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi import HTTPException
from datetime import date
from src.models.patient import Patient, Base
from src.services.patient_search import get_patients, get_patient_by_id


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


def populate_test_data(db):
    patients = [
        Patient(
            name="Jon Snow",
            birth_date=date(1990, 1, 1),
            health_conditions="Night Watch Trauma",
            gender="Male",
            address="Castle Black",
        ),
        Patient(
            name="Arya Stark",
            birth_date=date(1999, 6, 12),
            health_conditions="Blindness (temporary)",
            gender="Female",
            address="Braavos",
        ),
        Patient(
            name="Tyrion Lannister",
            birth_date=date(1980, 3, 10),
            health_conditions="Alcoholism",
            gender="Male",
            address="Casterly Rock",
        ),
    ]
    db.add_all(patients)
    db.commit()


def test_get_patients(test_db):
    populate_test_data(test_db)

    patients = get_patients(test_db)
    assert len(patients) == 3

    patients = get_patients(test_db, name="Jon")
    assert len(patients) == 1
    assert patients[0].name == "Jon Snow"

    patients = get_patients(test_db, health_conditions="Alcoholism")
    assert len(patients) == 1
    assert patients[0].name == "Tyrion Lannister"

    patients = get_patients(test_db, skip=1, limit=1)
    assert len(patients) == 1
    assert patients[0].name == "Arya Stark"

    patients = get_patients(test_db, patient_id=1)
    assert len(patients) == 1
    assert patients[0].name == "Jon Snow"


def test_get_patient_by_id(test_db):
    populate_test_data(test_db)

    patient = get_patient_by_id(test_db, 1)
    assert patient.name == "Jon Snow"

    with pytest.raises(HTTPException) as excinfo:
        get_patient_by_id(test_db, 9999)

    assert excinfo.value.status_code == 404
    assert excinfo.value.detail == "Paciente com ID 9999 não encontrado."
