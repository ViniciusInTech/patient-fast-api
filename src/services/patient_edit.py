from fastapi import HTTPException
from src.schemas.patient import Patient
from src.config.database import SessionLocal
from src.models.patient import PatientCreate
from src.services.patient_validations import validate_patient


def update_patient(patient_id: int, updated_data: PatientCreate):
    db = SessionLocal()
    try:
        db_patient = db.query(Patient).filter(Patient.id == patient_id).first()

        validate_patient(updated_data)
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
    finally:
        db.close()
