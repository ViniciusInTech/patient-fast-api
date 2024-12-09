from fastapi import APIRouter, Depends

from typing import Optional
from fastapi import HTTPException
from src.auth_dependencies import oauth2_scheme
from src.services.patient_service import PatientService
from src.schemas.patient import PatientCreate, Patient
from src.services.auth import validate_user
from src.services.patient_service import get_patient_service

router = APIRouter()


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
def add_patient(patient: PatientCreate, token: str = Depends(oauth2_scheme),
                patient_service: PatientService = Depends(get_patient_service)):
    validate_user(token)
    patient_new = patient_service.add_patient(patient)
    return patient_new


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
def edit_patient(patient_id: int, updated_data: PatientCreate, token: str = Depends(oauth2_scheme),
                 patient_service: PatientService = Depends(get_patient_service)):
    validate_user(token)
    patient_updated = patient_service.update_patient(patient_id, updated_data)
    if patient_updated is None:
        raise HTTPException(
            status_code=404,
            detail=f"Patient not found with ID {patient_id}. "
        )
    return patient_updated


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
def remove_patient(patient_id: int, token: str = Depends(oauth2_scheme),
                   patient_service: PatientService = Depends(get_patient_service)):
    validate_user(token)

    if patient_service.delete_patient_by_id(patient_id) is None:
        raise HTTPException(
            status_code=404,
            detail=f"Patient not found."
        )
    return {"message": f"Patient with id '{patient_id}' successfully deleted!"}


@router.get(
    "/patients/",
    response_model=list[Patient],
    summary="List patients with optional filters",
    description=(
            "Retrieve a list of patients with optional filters:\n\n"
            "- **name**: Filter by patient name (case-insensitive).\n"
            "- **health_conditions**: Filter by health conditions (case-insensitive).\n"
            "- **patient_id**: Filter by patient ID.\n\n"
            "Supports pagination using **skip** and **limit** parameters."
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
def list_patients(
        skip: int = 0,
        limit: int = 10,
        name: Optional[str] = None,
        birth_date: Optional[str] = None,
        health_conditions: Optional[str] = None,
        address: Optional[str] = None,
        token: str = Depends(oauth2_scheme),
        patient_service: PatientService = Depends(get_patient_service)):
    validate_user(token)
    return patient_service.get_patients(
        skip=skip,
        limit=limit,
        name=name,
        birth_date=birth_date,
        health_conditions=health_conditions,
        address=address,
    )


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
def get_patient(patient_id: int, token: str = Depends(oauth2_scheme),
                patient_service: PatientService = Depends(get_patient_service)):
    validate_user(token)
    return patient_service.get_patient_by_id(patient_id)
