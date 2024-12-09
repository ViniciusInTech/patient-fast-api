from fastapi import HTTPException
from sqlalchemy.orm import Session
from datetime import date
from src.schemas.patient import Patient
from src.models.patient import PatientCreate


def validate_patient(patient: PatientCreate):
    if patient.birth_date > date.today():
        raise HTTPException(
            status_code=400,
            detail="The date of birth cannot be a future date."
        )

    if len(patient.name.split()) < 2:
        raise HTTPException(
            status_code=400,
            detail="The name must contain at least two words."
        )

    valid_genders = ["Masculine", "Feminine"]
    if patient.gender.capitalize() not in valid_genders:
        raise HTTPException(
            status_code=400,
            detail=f"The gender must be one of the following: {', '.join(valid_genders)}."
        )


def validate_patient_creating(db: Session, patient: PatientCreate):
    validate_patient(patient)
    existing_patient = db.query(Patient).filter(
        Patient.name == patient.name,
        Patient.birth_date == patient.birth_date
    ).first()

    if existing_patient:
        raise HTTPException(
            status_code=400,
            detail="There is already a patient with that name and date of birth."
        )
