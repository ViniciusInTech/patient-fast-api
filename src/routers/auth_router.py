from fastapi import APIRouter
from src.models.user import UserCreate, UserLogin
from src.services.user_authenticate import authenticate_user
from src.services.user_create import create_user

router = APIRouter()


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
def register_user(user: UserCreate):
    create_user(user.username, user.password)
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
def login(user_login: UserLogin):
    token = authenticate_user(user_login.username, user_login.password)
    return {"access_token": token, "token_type": "bearer"}
