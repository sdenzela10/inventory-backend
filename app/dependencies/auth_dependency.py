from fastapi import Depends, Request

from app.core.config import settings
from app.core.security import decode_access_token
from app.dependencies.service_dependency import get_auth_service
from app.exceptions.auth_exception import InvalidTokenError
from app.services.auth_service import AuthService


def get_current_user(
    request: Request,
    auth_service: AuthService = Depends(get_auth_service),
):
    token = request.cookies.get(settings.auth_cookie_name)

    if not token:
        raise InvalidTokenError()

    try:
        payload = decode_access_token(token)
    except ValueError:
        raise InvalidTokenError()

    user_id = payload.get("sub")

    if not user_id:
        raise InvalidTokenError()

    return auth_service.get_authenticated_user(user_id)