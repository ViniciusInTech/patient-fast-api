from sqlalchemy.orm import Session
from fastapi import HTTPException
from src.models.patient import Patient


def delete_patient(db: Session, patient_id: int):
    db_patient = db.query(Patient).filter(Patient.id == patient_id).first()

    if not db_patient:
        raise HTTPException(
            status_code=404,
            detail="Patient not found."
        )

    db.delete(db_patient)
    db.commit()
    return {"detail": "Patient deleted successfully."}
