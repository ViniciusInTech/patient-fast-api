from fastapi import HTTPException
from typing import Optional
from sqlalchemy.orm import Session
from src.models.patient import Patient


def get_patients(
        db: Session,
        skip: int = 0,
        limit: int = 10,
        name: Optional[str] = None,
        health_conditions: Optional[str] = None,
        patient_id: Optional[int] = None,
):
    query = db.query(Patient)

    if patient_id:
        query = query.filter(Patient.id == patient_id)
    if name:
        query = query.filter(Patient.name.ilike(f"%{name}%"))
    if health_conditions:
        query = query.filter(Patient.health_conditions.ilike(f"%{health_conditions}%"))

    return query.offset(skip).limit(limit).all()


def get_patient_by_id(db: Session, patient_id: int):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()

    if not patient:
        raise HTTPException(
            status_code=404,
            detail=f"Paciente com ID {patient_id} não encontrado."
        )

    return patient
