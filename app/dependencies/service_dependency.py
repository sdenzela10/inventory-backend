from fastapi import Depends

from app.db.database import get_db
from app.repositories.user_repository import UserRepository
from app.services.auth_service import AuthService
from app.repositories.inventory_repository import InventoryRepository
from app.services.inventory_service import InventoryService


def get_auth_service(
    db=Depends(get_db),
) -> AuthService:
    user_repository = UserRepository(db)

    return AuthService(user_repository)


def get_inventory_service(
    db=Depends(get_db),
) -> InventoryService:
    inventory_repository = InventoryRepository(db)

    return InventoryService(inventory_repository)