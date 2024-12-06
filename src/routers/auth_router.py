from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.services.auth import hash_password, verify_password, create_access_token
from src.config.database import SessionLocal
from src.models.user import User
from src.schemas.user import UserCreate, UserLogin

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post(
    "/register/",
    summary="Register a new user",
    description=(
        "This endpoint allows registering a new user in the system by providing a username and password. "
        "The password will be securely hashed before being stored in the database."
    ),
    responses={
        200: {
            "description": "User successfully registered.",
            "content": {
                "application/json": {
                    "example": {"detail": "User successfully registered."}
                }
            },
        },
        409: {
            "description": "Username already exists.",
            "content": {
                "application/json": {
                    "example": {"detail": "The username is already in use."}
                }
            },
        },
    },
)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(
            status_code=409, detail="The username is already in use."
        )

    hashed_password = hash_password(user.password)
    new_user = User(username=user.username, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"detail": "User successfully registered."}


@router.post(
    "/login",
    summary="User login",
    description=(
        "This endpoint authenticates a user in the system. By providing a valid username and password, "
        "the system returns a JWT token that can be used to access protected routes."
    ),
    responses={
        200: {
            "description": "Login successful. Returns a valid JWT token.",
            "content": {
                "application/json": {
                    "example": {
                        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                        "token_type": "bearer",
                    }
                }
            },
        },
        401: {
            "description": "Invalid credentials.",
            "content": {
                "application/json": {
                    "example": {"detail": "Invalid credentials"}
                }
            },
        },
    },
)
def login(user_login: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == user_login.username).first()
    if not user or not verify_password(user_login.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}
