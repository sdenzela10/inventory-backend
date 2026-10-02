from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.logging import configure_logging
from app.routers.auth_router import router as auth_router
from app.routers.health_router import router as health_router
from app.routers.inventory_router import router as inventory_router
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
from app.exceptions.exception_handlers import (
    invalid_credentials_exception_handler,
    invalid_token_exception_handler,
    inventory_not_found_exception_handler,
    duplicate_item_name_exception_handler,
    duplicate_sku_exception_handler,
    invalid_stock_adjustment_exception_handler,
    csrf_exception_handler,
    unexpected_exception_handler,
)


configure_logging()


app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
)

cors_origins = [
    origin.strip()
    for origin in settings.cors_origins.split(",")
    if origin.strip()
]

cors_methods = [
    method.strip()
    for method in settings.cors_allowed_methods.split(",")
    if method.strip()
]

cors_headers = [
    header.strip()
    for header in settings.cors_allowed_headers.split(",")
    if header.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_methods=cors_methods,
    allow_headers=cors_headers,
    allow_credentials=True,
)

app.include_router(health_router)
app.include_router(auth_router)
app.include_router(inventory_router)

app.add_exception_handler(
    InvalidCredentialsError,
    invalid_credentials_exception_handler,
)

app.add_exception_handler(
    InvalidTokenError,
    invalid_token_exception_handler,
)

app.add_exception_handler(
    InventoryNotFoundError,
    inventory_not_found_exception_handler,
)

app.add_exception_handler(
    DuplicateItemNameError,
    duplicate_item_name_exception_handler,
)

app.add_exception_handler(
    DuplicateSKUError,
    duplicate_sku_exception_handler,
)

app.add_exception_handler(
    InvalidStockAdjustmentError,
    invalid_stock_adjustment_exception_handler,
)

app.add_exception_handler(
    CSRFError, 
    csrf_exception_handler,
)

app.add_exception_handler(
    Exception,
    unexpected_exception_handler,
)