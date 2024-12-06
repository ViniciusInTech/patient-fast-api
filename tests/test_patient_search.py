import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi import HTTPException
from src.models.patient import Patient, Base
from src.services.patient_search import get_patients, get_patient_by_id
from datetime import date

# Configurar o banco de dados em memória para testes
@pytest.fixture(scope="module")
def test_db():
    engine = create_engine("sqlite:///:memory:")
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)  # Criar tabelas do modelo no banco em memória
    db = SessionLocal()
    try:
        yield db  # Passa o banco simulado para os testes
    finally:
        db.close()


def populate_test_data(db):
    """
    Populate the database with Game of Thrones characters.
    """
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
    """
    Test retrieving patients with and without filters.
    """
    populate_test_data(test_db)

    # Test without filters
    patients = get_patients(test_db)
    assert len(patients) == 3

    # Test with name filter
    patients = get_patients(test_db, name="Jon")
    assert len(patients) == 1
    assert patients[0].name == "Jon Snow"

    # Test with health conditions filter
    patients = get_patients(test_db, health_conditions="Alcoholism")
    assert len(patients) == 1
    assert patients[0].name == "Tyrion Lannister"

    # Test with pagination
    patients = get_patients(test_db, skip=1, limit=1)
    assert len(patients) == 1
    assert patients[0].name == "Arya Stark"


def test_get_patient_by_id(test_db):
    """
    Test retrieving a patient by ID.
    """
    populate_test_data(test_db)

    # Test valid patient ID
    patient = get_patient_by_id(test_db, 1)  # ID is 1 for the first patient
    assert patient.name == "Jon Snow"

    # Test invalid patient ID
    with pytest.raises(HTTPException) as excinfo:
        get_patient_by_id(test_db, 9999)

    assert excinfo.value.status_code == 404
    assert excinfo.value.detail == "Paciente com ID 9999 não encontrado."
