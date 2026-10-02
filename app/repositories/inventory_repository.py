from datetime import datetime, timezone
from decimal import Decimal
from uuid import UUID

from sqlalchemy import select, update, func
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.models.inventory_model import InventoryItem


class InventoryRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_item(
        self,
        user_id: UUID,
        name: str,
        sku: str,
        quantity: int,
        price: Decimal,
        category: str,
        description: str | None = None,
    ) -> InventoryItem:
        item = InventoryItem(
            user_id=user_id,
            name=name,
            sku=sku,
            quantity=quantity,
            price=price,
            category=category,
            description=description,
        )

        self.db.add(item)

        try:
            self.db.commit()
        except IntegrityError:
            self.db.rollback()
            raise

        self.db.refresh(item)

        return item

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
    ) -> list[InventoryItem]:
        statement = select(InventoryItem).where(
            InventoryItem.user_id == user_id,
        )

        if category is not None:
            statement = statement.where(
                InventoryItem.category == category,
            )

        if search is not None:
            statement = statement.where(
                InventoryItem.name.ilike(f"%{search}%"),
            )

        if min_price is not None:
            statement = statement.where(
                InventoryItem.price >= min_price,
            )

        if max_price is not None:
            statement = statement.where(
                InventoryItem.price <= max_price,
            )

        if min_quantity is not None:
            statement = statement.where(
                InventoryItem.quantity >= min_quantity,
            )

        if max_quantity is not None:
            statement = statement.where(
                InventoryItem.quantity <= max_quantity,
            )

        statement = statement.offset(offset).limit(limit)

        return list(self.db.scalars(statement).all())

    def get_item(
        self,
        user_id: UUID,
        item_id: UUID,
    ) -> InventoryItem | None:
        statement = select(InventoryItem).where(
            InventoryItem.id == item_id,
            InventoryItem.user_id == user_id,
        )

        return self.db.scalar(statement)

    def update_item(
        self,
        user_id: UUID,
        item_id: UUID,
        name: str | None = None,
        sku: str | None = None,
        quantity: int | None = None,
        price: Decimal | None = None,
        category: str | None = None,
        description: str | None = None,
    ) -> InventoryItem | None:
        statement = select(InventoryItem).where(
            InventoryItem.id == item_id,
            InventoryItem.user_id == user_id,
        )

        item = self.db.scalar(statement)

        if item is None:
            return None

        if name is not None:
            item.name = name

        if sku is not None:
            item.sku = sku

        if quantity is not None:
            item.quantity = quantity

        if price is not None:
            item.price = price

        if category is not None:
            item.category = category

        if description is not None:
            item.description = description

        try:
            self.db.commit()
        except IntegrityError:
            self.db.rollback()
            raise

        self.db.refresh(item)

        return item

    def delete_item(
        self,
        user_id: UUID,
        item_id: UUID,
    ) -> bool:
        statement = select(InventoryItem).where(
            InventoryItem.id == item_id,
            InventoryItem.user_id == user_id,
        )

        item = self.db.scalar(statement)

        if item is None:
            return False

        self.db.delete(item)
        self.db.commit()

        return True

    def adjust_stock(
        self,
        user_id: UUID,
        item_id: UUID,
        quantity_delta: int,
    ) -> InventoryItem | None:
        statement = (
            update(InventoryItem)
            .where(
                InventoryItem.id == item_id,
                InventoryItem.user_id == user_id,
                InventoryItem.quantity + quantity_delta >= 0,
            )
            .values(
                quantity=InventoryItem.quantity + quantity_delta,
                updated_at=datetime.now(timezone.utc),
            )
            .returning(InventoryItem)
        )

        item = self.db.execute(statement).scalar_one_or_none()

        if item is None:
            self.db.rollback()
            return None

        self.db.commit()

        return item

    def get_dashboard_summary(
        self,
        user_id: UUID,
    ) -> tuple[int, int, Decimal]:
        statement = select(
            func.count(InventoryItem.id),
            func.coalesce(func.sum(InventoryItem.quantity), 0),
            func.coalesce(
                func.sum(
                    InventoryItem.quantity * InventoryItem.price
                ),
                0,
            ),
        ).where(
            InventoryItem.user_id == user_id,
        )

        total_items, total_quantity, total_inventory_value = (
            self.db.execute(statement).one()
        )

        return (
            total_items,
            total_quantity,
            total_inventory_value,
        )