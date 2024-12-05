from fastapi import FastAPI
from src.config.database import Base, engine
from src.routers.patient_router import router as patient_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(patient_router, prefix="/api")
