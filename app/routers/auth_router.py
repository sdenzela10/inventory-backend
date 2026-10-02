from fastapi import APIRouter, Depends, Response

from app.core.config import settings
from app.core.csrf import generate_csrf_token, set_csrf_cookie
from app.dependencies.auth_dependency import get_current_user
from app.dependencies.service_dependency import get_auth_service
from app.dependencies.csrf_dependency import validate_csrf
from app.schemas.auth_schema import (
    AuthenticatedUser,
    UserLogin,
    UserRegistration,
)
from app.services.auth_service import AuthService


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/register",
    response_model=AuthenticatedUser,
)
def register(
    data: UserRegistration,
    auth_service: AuthService = Depends(get_auth_service),
):
    return auth_service.register(data)


@router.post("/login")
def login(
    data: UserLogin,
    response: Response,
    auth_service: AuthService = Depends(get_auth_service),
):
    token = auth_service.login(data)

    response.set_cookie(
        key=settings.auth_cookie_name,
        value=token,
        secure=settings.cookie_secure,
        httponly=settings.cookie_httponly,
        samesite=settings.cookie_samesite,
    )

    csrf_token = generate_csrf_token()
    set_csrf_cookie(response, csrf_token)

    return {"message": "Login successful"}


@router.post(
    "/logout",
    dependencies=[Depends(validate_csrf)]
)
def logout(response: Response):
    response.delete_cookie(
        key=settings.auth_cookie_name,
    )

    return {"message": "Logout successful"}


@router.get(
    "/me",
    response_model=AuthenticatedUser,
)
def get_me(
    current_user: AuthenticatedUser = Depends(get_current_user),
):
    return current_user