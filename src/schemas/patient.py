from pydantic import BaseModel
from datetime import date


class PatientBase(BaseModel):
    name: str
    birth_date: date
    health_conditions: str
    gender: str
    address: str


class PatientCreate(PatientBase):
    pass


class Patient(PatientBase):
    id: int

    class Config:
        orm_mode = True
