from uuid import UUID, uuid4

from datetime import datetime, timezone

from decimal import Decimal

from sqlalchemy import (
    ForeignKey,
    String,
    UniqueConstraint,
    CheckConstraint,
    Integer,
    Numeric,
    DateTime,
    )
from sqlalchemy import UUID as SQLAlchemyUUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class InventoryItem(Base):
    __tablename__ = "inventory_items"

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "sku",
            name="uq_inventory_items_user_id_sku",
        ),
         UniqueConstraint(
            "user_id",
            "name",
            name="uq_inventory_items_user_id_name",
        ),
        CheckConstraint(
            "quantity >= 0",
            name="ck_inventory_items_quantity_nonnegative",
        ),
        CheckConstraint(
            "price >= 0",
            name="ck_inventory_items_price_nonnegative",
        ),
    )

    id: Mapped[UUID] = mapped_column(
        SQLAlchemyUUID,
        primary_key=True,
        default=uuid4,
        nullable=False,
    )

    user_id: Mapped[UUID] = mapped_column(
        SQLAlchemyUUID,
        ForeignKey(
            "users.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    sku: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    quantity: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    price: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )

    category: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        String(1000),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )