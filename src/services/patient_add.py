from src.config.database import SessionLocal
from src.schemas.patient import Patient
from src.models.patient import PatientCreate
from src.services.patient_validations import validate_patient_creating


def create_patient(patient: PatientCreate):
    db = SessionLocal()
    try:

        validate_patient_creating(db, patient)

        db_patient = Patient(**patient.dict())
        db.add(db_patient)
        db.commit()
        db.refresh(db_patient)
        return db_patient
    finally:
        db.close()
