from fastapi import HTTPException
from typing import Optional
from src.config.database import SessionLocal
from src.schemas.patient import Patient


def get_patients(
        skip: int = 0,
        limit: int = 10,
        name: Optional[str] = None,
        health_conditions: Optional[str] = None,
):
    db = SessionLocal()
    try:
        query = db.query(Patient)

        if name:
            query = query.filter(Patient.name.ilike(f"%{name}%"))
        if health_conditions:
            query = query.filter(Patient.health_conditions.ilike(f"%{health_conditions}%"))

        return query.offset(skip).limit(limit).all()
    finally:
        db.close()


def get_patient_by_id(patient_id: int):
    db = SessionLocal()
    try:
        patient = db.query(Patient).filter(Patient.id == patient_id).first()

        if not patient:
            raise HTTPException(
                status_code=404,
                detail=f"Patient with ID {patient_id} not found."
            )

        return patient
    finally:
        db.close()
