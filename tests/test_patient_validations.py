import pytest
from fastapi import HTTPException
from datetime import date
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.models.patient import Patient, Base
from src.schemas.patient import PatientCreate
from src.services.patient_validations import validate_patient


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
            gender="Masculino",
            address="Castle Black",
        ),
        Patient(
            name="Arya Stark",
            birth_date=date(1999, 6, 12),
            health_conditions="Blindness (temporary)",
            gender="Feminino",
            address="Braavos",
        ),
    ]
    db.add_all(patients)
    db.commit()


def test_validate_patient_valid(test_db):
    patient_data = PatientCreate(
        name="Daenerys Targaryen",
        birth_date="1990-06-25",
        health_conditions="Fire Immunity",
        gender="Feminino",
        address="Dragonstone",
    )

    validate_patient(test_db, patient_data)


def test_validate_patient_future_birth_date(test_db):
    patient_data = PatientCreate(
        name="Robb Stark",
        birth_date="2090-06-15",
        health_conditions="King in the North",
        gender="Masculino",
        address="Winterfell",
    )

    with pytest.raises(HTTPException) as excinfo:
        validate_patient(test_db, patient_data)

    assert excinfo.value.status_code == 400
    assert excinfo.value.detail == "A data de nascimento não pode ser uma data futura."


def test_validate_patient_single_word_name(test_db):
    patient_data = PatientCreate(
        name="Jon",
        birth_date="1990-01-01",
        health_conditions="Winter is Coming",
        gender="Masculino",
        address="Castle Black",
    )

    with pytest.raises(HTTPException) as excinfo:
        validate_patient(test_db, patient_data)

    assert excinfo.value.status_code == 400
    assert excinfo.value.detail == "O nome deve conter pelo menos duas palavras."


def test_validate_patient_invalid_gender(test_db):
    patient_data = PatientCreate(
        name="Samwell Tarly",
        birth_date="1990-12-23",
        health_conditions="Heavyweight",
        gender="Other",
        address="Horn Hill",
    )

    with pytest.raises(HTTPException) as excinfo:
        validate_patient(test_db, patient_data)

    assert excinfo.value.status_code == 400
    assert excinfo.value.detail == "O gênero deve ser um dos seguintes: Masculino, Feminino."


def test_validate_patient_existing_patient(test_db):
    populate_test_data(test_db)

    patient_data = PatientCreate(
        name="Jon Snow",
        birth_date="1990-01-01",
        health_conditions="Night Watch Trauma",
        gender="Masculino",
        address="Castle Black",
    )

    with pytest.raises(HTTPException) as excinfo:
        validate_patient(test_db, patient_data)

    assert excinfo.value.status_code == 400
    assert excinfo.value.detail == "Já existe um paciente com esse nome e data de nascimento."
