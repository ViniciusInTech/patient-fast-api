from fastapi import HTTPException
from src.schemas.user import User
from src.config.database import SessionLocal
from src.services.auth import verify_password, create_access_token


def authenticate_user(username: str, password: str):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.username == username).first()
        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        return create_access_token({"sub": user.username})
    finally:
        db.close()
