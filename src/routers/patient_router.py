from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.services.patient_add import create_patient
from src.services.patient_search import get_patients
from src.services.patient_edit import update_patient
from src.services.patient_delete import delete_patient
from src.services.patient_search import get_patient_by_id
from src.config.database import SessionLocal
from src.schemas.patient import PatientCreate, Patient

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/patients/", response_model=Patient)
def add_patient(patient: PatientCreate, db: Session = Depends(get_db)):
    return create_patient(db, patient)


@router.put("/patients/{patient_id}", response_model=Patient)
def edit_patient(patient_id: int, updated_data: PatientCreate, db: Session = Depends(get_db)):
    return update_patient(db, patient_id, updated_data)


@router.delete("/patients/{patient_id}")
def remove_patient(patient_id: int, db: Session = Depends(get_db)):
    return delete_patient(db, patient_id)


@router.get("/patients/", response_model=list[Patient])
def list_patients(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_patients(db, skip, limit)


@router.get("/patients/{patient_id}", response_model=Patient)
def get_patient(patient_id: int, db: Session = Depends(get_db)):
    return get_patient_by_id(db, patient_id)
