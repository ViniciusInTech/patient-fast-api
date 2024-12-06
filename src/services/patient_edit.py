from sqlalchemy.orm import Session
from fastapi import HTTPException
from src.models.patient import Patient
from src.schemas.patient import PatientCreate


def update_patient(db: Session, patient_id: int, updated_data: PatientCreate):
    db_patient = db.query(Patient).filter(Patient.id == patient_id).first()

    if not db_patient:
        raise HTTPException(
            status_code=404,
            detail=f"Patient not found with ID {patient_id}. "
        )

    for key, value in updated_data.dict().items():
        setattr(db_patient, key, value)

    db.commit()
    db.refresh(db_patient)
    return db_patient
