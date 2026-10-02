from fastapi import Request
from fastapi.responses import JSONResponse

import logging

from app.exceptions.auth_exception import (
    InvalidCredentialsError,
    InvalidTokenError,
)
from app.exceptions.inventory_exception import (
    DuplicateItemNameError,
    DuplicateSKUError,
    InvalidStockAdjustmentError,
    InventoryNotFoundError,
)
from app.exceptions.csrf_exception import CSRFError
from app.schemas.error_schema import ErrorResponse


logger = logging.getLogger(__name__)


async def invalid_credentials_exception_handler(
    request: Request,
    exc: InvalidCredentialsError,
) -> JSONResponse:
    error = ErrorResponse(
        detail="Invalid credentials",
    )

    return JSONResponse(
        status_code=401,
        content=error.model_dump(),
    )


async def invalid_token_exception_handler(
    request: Request,
    exc: InvalidTokenError,
) -> JSONResponse:
    error = ErrorResponse(
        detail="Invalid or expired token",
    )

    return JSONResponse(
        status_code=401,
        content=error.model_dump(),
    )


async def inventory_not_found_exception_handler(
    request: Request,
    exc: InventoryNotFoundError,
) -> JSONResponse:
    error = ErrorResponse(
        detail="Inventory item not found",
    )

    return JSONResponse(
        status_code=404,
        content=error.model_dump(),
    )


async def duplicate_item_name_exception_handler(
    request: Request,
    exc: DuplicateItemNameError,
) -> JSONResponse:
    error = ErrorResponse(detail="Inventory item name already exists")
    return JSONResponse(status_code=409, content=error.model_dump())


async def duplicate_sku_exception_handler(
    request: Request,
    exc: DuplicateSKUError,
) -> JSONResponse:
    error = ErrorResponse(
        detail="SKU already exists",
    )

    return JSONResponse(
        status_code=409,
        content=error.model_dump(),
    )


async def invalid_stock_adjustment_exception_handler(
    request: Request,
    exc: InvalidStockAdjustmentError,
) -> JSONResponse:
    error = ErrorResponse(
        detail="Invalid stock adjustment",
    )

    return JSONResponse(
        status_code=400,
        content=error.model_dump(),
    )


async def csrf_exception_handler(
    request: Request,
    exc: CSRFError,
) -> JSONResponse:
    return JSONResponse(
        status_code=403,
        content={
            "detail": "CSRF validation failed",
        },
    )


async def unexpected_exception_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    logger.exception(
        "Unexpected application error: %s %s",
        request.method,
        request.url.path,
    )

    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
        },
    )