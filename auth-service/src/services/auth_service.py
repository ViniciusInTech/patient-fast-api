from passlib.hash import bcrypt
from src.repositories.user_repository import UserRepository
from src.models.user import User
from src.schemas.auth import RegisterRequest, LoginRequest
from src.services.token_service import create_access_token
from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import Session
from src.config.database import get_db


class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.user_repo = UserRepository(db)

    def register(self, request: RegisterRequest):
        if self.user_repo.get_user_by_email(request.email):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

        hashed_password = bcrypt.hash(request.password)
        new_user = User(name=request.name, email=request.email, hashed_password=hashed_password)
        self.user_repo.create_user(new_user)

        return {"message": "User registered successfully"}

    def login(self, request: LoginRequest):
        user = self.user_repo.get_user_by_email(request.email)
        if not user or not bcrypt.verify(request.password, user.hashed_password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

        token = create_access_token(data={"sub": user.email})
        return {"access_token": token, "token_type": "bearer"}


def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    return AuthService(db)
