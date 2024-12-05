from sqlalchemy.orm import Session
from src.models.patient import Patient
from src.schemas.patient import PatientCreate
from src.services.patient_validations import validate_patient


def create_patient(db: Session, patient: PatientCreate):
    validate_patient(db, patient)

    db_patient = Patient(**patient.dict())
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient
