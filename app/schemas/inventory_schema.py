from datetime import datetime
from decimal import Decimal
from uuid import UUID

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class InventoryCreate(BaseModel):
    name: str = Field(min_length=1)
    sku: str = Field(min_length=1)
    quantity: int = Field(ge=0)
    price: Decimal = Field(ge=0)
    category: str
    description: str | None = None


class InventoryUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1)
    sku: str | None = Field(default=None, min_length=1)
    quantity: int | None = Field(default=None, ge=0)
    price: Decimal | None = Field(default=None, ge=0)
    category: str | None = None
    description: str | None = None


class InventoryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID
    name: str
    sku: str
    quantity: int
    price: Decimal
    category: str
    description: str | None
    created_at: datetime
    updated_at: datetime


class InventoryListQuery(BaseModel):
    category: str | None = None
    search: str | None = None
    min_price: Decimal | None = Field(default=None, ge=0)
    max_price: Decimal | None = Field(default=None, ge=0)
    min_quantity: int | None = Field(default=None, ge=0)
    max_quantity: int | None = Field(default=None, ge=0)
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=100)


class StockAdjustment(BaseModel):
    quantity: int = Field(ge=0)
    operation: Literal["in", "out"]


class InventoryDashboardSummary(BaseModel):
    total_items: int
    total_quantity: int
    total_inventory_value: Decimal