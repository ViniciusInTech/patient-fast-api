from sqlalchemy.orm import Session
from src.models.patient import Patient
from src.schemas.patient import PatientCreate
from typing import Optional, Dict, Any


class PatientRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_patient_by_id(self, patient_id: int):
        return self.db.query(Patient).filter(Patient.id == patient_id).first()

    def create_patient(self, patient: PatientCreate):
        db_patient = Patient(**patient.dict())
        self.db.add(db_patient)
        self.db.commit()
        self.db.refresh(db_patient)
        return db_patient

    def update_patient(self, patient_id: int, patient_data: PatientCreate):
        db_patient = self.db.query(Patient).filter(Patient.id == patient_id).first()
        if db_patient:
            for key, value in patient_data.dict().items():
                setattr(db_patient, key, value)
            self.db.commit()
            self.db.refresh(db_patient)
            return db_patient
        return None

    def delete_patient_by_id(self, patient_id: int):
        db_patient = self.db.query(Patient).filter(Patient.id == patient_id).first()
        if db_patient:
            self.db.delete(db_patient)
            self.db.commit()
            return db_patient
        return None

    def get_patients(
            self,
            skip: int = 0,
            limit: int = 10,
            name: Optional[str] = None,
            birth_date: Optional[str] = None,
            health_conditions: Optional[str] = None,
            address: Optional[str] = None
    ):
        query = self.db.query(Patient)

        if name:
            query = query.filter(Patient.name.ilike(f"%{name}%"))
        if birth_date:
            query = query.filter(Patient.birth_date == birth_date)
        if health_conditions:
            query = query.filter(Patient.health_conditions.ilike(f"%{health_conditions}%"))
        if address:
            query = query.filter(Patient.address.ilike(f"%{address}%"))

        return query.offset(skip).limit(limit).all()
