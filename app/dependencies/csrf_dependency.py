from fastapi import Header, Request

from app.core.config import settings
from app.core.csrf import validate_csrf_token
from app.exceptions.csrf_exception import CSRFError


def validate_csrf(
    request: Request,
    csrf_header: str | None = Header(
        default=None,
        alias=settings.csrf_header_name,
    ),
) -> None:
    if request.method in {"GET", "HEAD", "OPTIONS"}:
        return

    csrf_cookie = request.cookies.get(settings.csrf_cookie_name)

    if not validate_csrf_token(csrf_cookie, csrf_header):
        raise CSRFError()