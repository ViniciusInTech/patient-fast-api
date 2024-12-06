from fastapi import HTTPException
from sqlalchemy.orm import Session
from src.models.user import User
from src.services.auth import hash_password, verify_password, create_access_token


def create_user(db: Session, username: str, password: str):
    hashed_password = hash_password(password)
    new_user = User(username=username, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def authenticate_user(db: Session, username: str, password: str):
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return create_access_token({"sub": user.username})
