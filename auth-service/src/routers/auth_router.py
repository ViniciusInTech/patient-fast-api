from fastapi import APIRouter, Depends
from src.schemas.auth import RegisterRequest, LoginRequest, Token
from src.services.auth_service import AuthService, get_auth_service

router = APIRouter()


@router.post("/register")
def register(request: RegisterRequest, auth_service: AuthService = Depends(get_auth_service)):
    return auth_service.register(request)


@router.post("/login", response_model=Token)
def login(request: LoginRequest, auth_service: AuthService = Depends(get_auth_service)):
    return auth_service.login(request)
