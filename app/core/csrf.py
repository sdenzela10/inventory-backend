import secrets

from fastapi import Response

from app.core.config import settings


def generate_csrf_token() -> str:
    return secrets.token_urlsafe(32)


def set_csrf_cookie(response: Response, token: str) -> None:
    response.set_cookie(
        key=settings.csrf_cookie_name,
        value=token,
        secure=settings.cookie_secure,
        httponly=False,
        samesite=settings.cookie_samesite,
    )


def validate_csrf_token(
    csrf_cookie: str | None,
    csrf_header: str | None,
) -> bool:
    if not csrf_cookie or not csrf_header:
        return False

    return secrets.compare_digest(csrf_cookie, csrf_header)