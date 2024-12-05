from fastapi import HTTPException
from sqlalchemy.orm import Session
from datetime import date
from src.models.patient import Patient
from src.schemas.patient import PatientCreate


def validate_patient(db: Session, patient: PatientCreate):
    if patient.birth_date > date.today():
        raise HTTPException(
            status_code=400,
            detail="A data de nascimento não pode ser uma data futura."
        )

    if len(patient.name.split()) < 2:
        raise HTTPException(
            status_code=400,
            detail="O nome deve conter pelo menos duas palavras."
        )

    valid_genders = ["Masculino", "Feminino"]
    if patient.gender.capitalize() not in valid_genders:
        raise HTTPException(
            status_code=400,
            detail=f"O gênero deve ser um dos seguintes: {', '.join(valid_genders)}."
        )

    existing_patient = db.query(Patient).filter(
        Patient.name == patient.name,
        Patient.birth_date == patient.birth_date
    ).first()

    if existing_patient:
        raise HTTPException(
            status_code=400,
            detail="Já existe um paciente com esse nome e data de nascimento."
        )
