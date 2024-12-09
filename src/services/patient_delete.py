from fastapi import HTTPException
from src.config.database import SessionLocal
from src.schemas.patient import Patient


def delete_patient(patient_id: int):
    db = SessionLocal()
    try:
        db_patient = db.query(Patient).filter(Patient.id == patient_id).first()

        if not db_patient:
            raise HTTPException(
                status_code=404,
                detail="Patient not found."
            )

        db.delete(db_patient)
        db.commit()
        return {"detail": "Patient deleted successfully."}
    finally:
        db.close()
