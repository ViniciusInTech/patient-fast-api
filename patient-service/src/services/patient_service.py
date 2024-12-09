from sqlalchemy.orm import Session
from src.schemas.patient import PatientCreate
from src.services.patient_validations import validate_patient_creating, validate_patient
from src.config.database import get_db
from fastapi import Depends
from typing import Optional, List

from src.repositories.patient_repository import PatientRepository


class PatientService:
    def __init__(self, db: Session):
        self.db = db
        self.patient_repo = PatientRepository(db)

    def add_patient(self, patient: PatientCreate):
        validate_patient_creating(self.db, patient)
        return self.patient_repo.create_patient(patient)

    def delete_patient_by_id(self, patient_id: int):
        return self.patient_repo.delete_patient_by_id(patient_id)

    def update_patient(self, patient_id: int, patient_data: PatientCreate):
        validate_patient(patient_data)
        return self.patient_repo.update_patient(patient_id, patient_data)

    def get_patient_by_id(self, patient_id: int):
        return self.patient_repo.get_patient_by_id(patient_id)

    def get_patients(
            self,
            skip: int = 0,
            limit: int = 10,
            name: Optional[str] = None,
            birth_date: Optional[str] = None,
            health_conditions: Optional[str] = None,
            address: Optional[str] = None
    ) -> List:

        return self.patient_repo.get_patients(
            skip=skip,
            limit=limit,
            name=name,
            birth_date=birth_date,
            health_conditions=health_conditions,
            address=address
        )


def get_patient_service(db: Session = Depends(get_db)) -> PatientService:
    return PatientService(db)

