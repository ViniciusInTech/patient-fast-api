from fastapi import HTTPException
from src.schemas.user import User
from src.config.database import SessionLocal
from src.services.auth import hash_password


def create_user(username: str, password: str):
    db = SessionLocal()
    try:
        existing_user = db.query(User).filter(User.username == username).first()
        if existing_user:
            raise HTTPException(
                status_code=409, detail="The username is already in use."
            )

        hashed_password = hash_password(password)
        new_user = User(username=username, hashed_password=hashed_password)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    finally:
        db.close()
