from decimal import Decimal
from uuid import UUID

from sqlalchemy.exc import IntegrityError

from app.repositories.inventory_repository import InventoryRepository
from app.schemas.inventory_schema import InventoryCreate, InventoryUpdate
from app.exceptions.inventory_exception import (
    DuplicateItemNameError,
    DuplicateSKUError,
    InvalidStockAdjustmentError,
    InventoryNotFoundError,
)


def _translate_integrity_error(exc: IntegrityError) -> None:
    constraint = getattr(exc.orig, "diag", None)

    if constraint is not None:
        constraint_name = getattr(constraint, "constraint_name", None)

        if constraint_name == "uq_inventory_items_user_id_sku":
            raise DuplicateSKUError() from exc

        if constraint_name == "uq_inventory_items_user_id_name":
            raise DuplicateItemNameError() from exc

    raise exc


class InventoryService:
    def __init__(self, inventory_repository: InventoryRepository):
        self.inventory_repository = inventory_repository

    def create_item(
        self,
        user_id: UUID,
        data: InventoryCreate,
    ):
        try:
            return self.inventory_repository.create_item(
                user_id=user_id,
                name=data.name,
                sku=data.sku,
                quantity=data.quantity,
                price=data.price,
                category=data.category,
                description=data.description,
            )
        except IntegrityError as exc:
            _translate_integrity_error(exc)

    def list_items(
        self,
        user_id: UUID,
        category: str | None = None,
        search: str | None = None,
        min_price: Decimal | None = None,
        max_price: Decimal | None = None,
        min_quantity: int | None = None,
        max_quantity: int | None = None,
        offset: int = 0,
        limit: int = 20,
    ):
        return self.inventory_repository.list_items(
            user_id=user_id,
            category=category,
            search=search,
            min_price=min_price,
            max_price=max_price,
            min_quantity=min_quantity,
            max_quantity=max_quantity,
            offset=offset,
            limit=limit,
        )

    def get_item(
        self,
        user_id: UUID,
        item_id: UUID,
    ):
        item = self.inventory_repository.get_item(
            user_id=user_id,
            item_id=item_id,
        )

        if item is None:
            raise InventoryNotFoundError()

        return item

    def update_item(
        self,
        user_id: UUID,
        item_id: UUID,
        data: InventoryUpdate,
    ):
        try:
            item = self.inventory_repository.update_item(
                user_id=user_id,
                item_id=item_id,
                name=data.name,
                sku=data.sku,
                quantity=data.quantity,
                price=data.price,
                category=data.category,
                description=data.description,
            )
        except IntegrityError as exc:
            _translate_integrity_error(exc)

        if item is None:
            raise InventoryNotFoundError()

        return item

    def delete_item(
        self,
        user_id: UUID,
        item_id: UUID,
    ):
        deleted = self.inventory_repository.delete_item(
            user_id=user_id,
            item_id=item_id,
        )

        if not deleted:
            raise InventoryNotFoundError()

        return True

    def stock_in(
        self,
        user_id: UUID,
        item_id: UUID,
        quantity: int,
    ):
        item = self.inventory_repository.adjust_stock(
            user_id=user_id,
            item_id=item_id,
            quantity_delta=quantity,
        )

        if item is None:
            raise InvalidStockAdjustmentError()

        return item

    def stock_out(
        self,
        user_id: UUID,
        item_id: UUID,
        quantity: int,
    ):
        item = self.inventory_repository.adjust_stock(
            user_id=user_id,
            item_id=item_id,
            quantity_delta=-quantity,
        )

        if item is None:
            raise InvalidStockAdjustmentError()

        return item

    def get_dashboard_summary(
        self,
        user_id: UUID,
    ):
        return self.inventory_repository.get_dashboard_summary(
            user_id=user_id,
        )