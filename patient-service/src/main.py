from fastapi import FastAPI
from src.config.database import Base, engine
from src.routers.patient_router import router as patient_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
title="API de Gestão de Pacientes",
    description=(
        "Esta API permite gerenciar pacientes com funcionalidades de autenticação e proteção de rotas."
        " Use esta documentação para entender os endpoints disponíveis."
    ),
    version="1.0.0",
    contact={
        "name": "Carlos Vinicius",
        "email": " cvs1@poli.br",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
)

app.include_router(patient_router, prefix="/api")
