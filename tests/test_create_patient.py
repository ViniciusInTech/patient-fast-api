import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.models.patient import Patient, Base
from src.schemas.patient import PatientCreate
from src.services.patient_add import create_patient
from datetime import date


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


def test_create_patient_valid(test_db):
    patient_data = PatientCreate(
        name="John Snow",
        birth_date="1990-01-01",
        health_conditions="Cancer",
        gender="Masculino",
        address="Reino do Norte",
    )

    patient = create_patient(test_db, patient_data)

    assert patient.id is not None
    assert patient.name == "John Snow"
    assert patient.birth_date == date(1990, 1, 1)
    assert patient.health_conditions == "Cancer"
    assert patient.gender == "Masculino"
    assert patient.address == "Reino do Norte"


def test_create_patient_invalid(test_db):
    invalid_patient = PatientCreate(
        name="Bruno mars",
        birth_date="9090-01-01",
        health_conditions="diabetes",
        gender="Feminino",
        address="casa branca",
    )

    with pytest.raises(Exception) as excinfo:
        create_patient(test_db, invalid_patient)

    assert "A data de nascimento não pode ser uma data futura." in str(excinfo.value)
