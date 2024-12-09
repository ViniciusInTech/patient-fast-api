from fastapi import FastAPI
from src.routers import auth_router
from src.config.database import engine, Base

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(auth_router.router, prefix="/api")


@app.get("/")
def read_root():
    return {"message": "Welcome to the Auth Service!"}
