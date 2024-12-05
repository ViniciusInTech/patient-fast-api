from fastapi import HTTPException
from sqlalchemy.orm import Session
from src.models.patient import Patient


def get_patients(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Patient).offset(skip).limit(limit).all()


def get_patient_by_id(db: Session, patient_id: int):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()

    if not patient:
        raise HTTPException(
            status_code=404,
            detail=f"Paciente com ID {patient_id} não encontrado."
        )

    return patient
