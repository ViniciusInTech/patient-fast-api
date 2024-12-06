from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.dependencies import oauth2_scheme
from src.services.patient_add import create_patient
from src.services.patient_search import get_patients
from src.services.patient_edit import update_patient
from src.services.patient_delete import delete_patient
from src.services.patient_search import get_patient_by_id
from src.config.database import SessionLocal
from src.schemas.patient import PatientCreate, Patient
from src.services.auth import validate_user

router = APIRouter()


def get_db():
    """Dependency to provide a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post(
    "/patients/",
    response_model=Patient,
    summary="Add a new patient",
    description=(
        "This endpoint allows adding a new patient to the system. "
        "The following fields are required in the request body:\n\n"
        "- **name**: Full name of the patient (e.g., 'John Doe').\n"
        "- **birth_date**: Date of birth in ISO format (e.g., '1990-01-01'). Must be earlier than the current date.\n"
        "- **health_conditions**: Description of the patient's health conditions (e.g., 'Hypertension').\n"
        "- **gender**: Patient's gender ('Male' or 'Female').\n"
        "- **address**: Full address of the patient.\n\n"
        "A valid JWT token must be provided in the Authorization header to access this endpoint."
    ),
    responses={
        200: {
            "description": "Patient successfully added.",
            "content": {"application/json": {"example": {"id": 1, "name": "John Doe"}}},
        },
        401: {
            "description": "Unauthorized - Invalid or missing token.",
            "content": {"application/json": {"example": {"detail": "Not authenticated"}}},
        },
    },
)
def add_patient(patient: PatientCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    validate_user(token)
    patient_new = create_patient(db, patient)
    return patient_new  # Return the full Patient object


@router.put(
    "/patients/{patient_id}",
    response_model=Patient,
    summary="Edit patient information",
    description=(
        "This endpoint allows updating the information of an existing patient, identified by the **ID** provided in the URL. "
        "The following fields can be updated in the request body:\n\n"
        "- **name**: Full name of the patient.\n"
        "- **birth_date**: Date of birth (must be earlier than the current date).\n"
        "- **health_conditions**: Patient's health conditions.\n"
        "- **gender**: Gender ('Male' or 'Female').\n"
        "- **address**: Address.\n\n"
        "A valid JWT token must be provided in the Authorization header."
    ),
    responses={
        200: {
            "description": "Patient successfully updated.",
            "content": {"application/json": {"example": {"id": 1, "name": "John Doe"}}},
        },
        401: {
            "description": "Unauthorized - Invalid or missing token.",
            "content": {"application/json": {"example": {"detail": "Not authenticated"}}},
        },
        404: {
            "description": "Patient not found.",
            "content": {
                "application/json": {"example": {"detail": "Patient with id '1' not found."}}
            },
        },
    },
)
def edit_patient(patient_id: int, updated_data: PatientCreate, db: Session = Depends(get_db),
                 token: str = Depends(oauth2_scheme)):
    validate_user(token)
    patient_updated = update_patient(db, patient_id, updated_data)
    return patient_updated  # Return the full Patient object


@router.delete(
    "/patients/{patient_id}",
    summary="Delete a patient",
    description=(
        "This endpoint allows deleting a patient from the system. "
        "The patient is identified by the **ID** provided in the URL. "
        "Ensure that a valid JWT token is included in the Authorization header."
    ),
    responses={
        200: {
            "description": "Patient successfully deleted.",
            "content": {"application/json": {"example": {"message": "Patient with id '1' successfully deleted!"}}},
        },
        401: {
            "description": "Unauthorized - Invalid or missing token.",
            "content": {"application/json": {"example": {"detail": "Not authenticated"}}},
        },
        404: {
            "description": "Patient not found.",
            "content": {
                "application/json": {"example": {"detail": "Patient with id '1' not found."}}
            },
        },
    },
)
def remove_patient(patient_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    validate_user(token)
    delete_patient(db, patient_id)
    return {"message": f"Patient with id '{patient_id}' successfully deleted!"}


@router.get(
    "/patients/",
    response_model=list[Patient],
    summary="List all patients",
    description=(
        "This endpoint retrieves a list of registered patients in the system. "
        "You can use the following query parameters for pagination:\n\n"
        "- **skip**: Number of patients to skip (default: 0).\n"
        "- **limit**: Maximum number of patients to return (default: 10).\n\n"
        "A valid JWT token must be provided in the Authorization header."
    ),
    responses={
        200: {
            "description": "List of patients retrieved successfully.",
            "content": {"application/json": {"example": [{"id": 1, "name": "John Doe"}]}},
        },
        401: {
            "description": "Unauthorized - Invalid or missing token.",
            "content": {"application/json": {"example": {"detail": "Not authenticated"}}},
        },
    },
)
def list_patients(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    validate_user(token)
    return get_patients(db, skip, limit)


@router.get(
    "/patients/{patient_id}",
    response_model=Patient,
    summary="Get patient details",
    description=(
        "This endpoint retrieves the details of a specific patient, identified by the **ID** provided in the URL. "
        "A valid JWT token must be provided in the Authorization header."
    ),
    responses={
        200: {
            "description": "Patient details retrieved successfully.",
            "content": {"application/json": {"example": {"id": 1, "name": "John Doe"}}},
        },
        401: {
            "description": "Unauthorized - Invalid or missing token.",
            "content": {"application/json": {"example": {"detail": "Not authenticated"}}},
        },
        404: {
            "description": "Patient not found.",
            "content": {
                "application/json": {"example": {"detail": "Patient with id '1' not found."}}
            },
        },
    },
)
def get_patient(patient_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    validate_user(token)
    return get_patient_by_id(db, patient_id)
