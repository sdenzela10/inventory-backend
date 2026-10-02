from decimal import Decimal
from uuid import UUID

from fastapi import APIRouter, Depends

from app.dependencies.auth_dependency import get_current_user
from app.dependencies.service_dependency import get_inventory_service
from app.dependencies.csrf_dependency import validate_csrf
from app.schemas.inventory_schema import (
    InventoryCreate,
    InventoryDashboardSummary,
    InventoryResponse,
    InventoryUpdate,
    StockAdjustment,
)
from app.services.inventory_service import InventoryService


router = APIRouter(
    tags=["Inventory"],
)


@router.post(
    "/inventory",
    dependencies=[Depends(validate_csrf)],
    response_model=InventoryResponse,
)
def create_inventory_item(
    data: InventoryCreate,
    current_user=Depends(get_current_user),
    inventory_service: InventoryService = Depends(get_inventory_service),
):
    return inventory_service.create_item(
        user_id=current_user.id,
        data=data,
    )


@router.get(
    "/inventory",
    response_model=list[InventoryResponse],
)
def list_inventory_items(
    category: str | None = None,
    search: str | None = None,
    min_price: Decimal | None = None,
    max_price: Decimal | None = None,
    min_quantity: int | None = None,
    max_quantity: int | None = None,
    page: int = 1,
    page_size: int = 20,
    current_user=Depends(get_current_user),
    inventory_service: InventoryService = Depends(get_inventory_service),
):
    offset = (page - 1) * page_size

    return inventory_service.list_items(
        user_id=current_user.id,
        category=category,
        search=search,
        min_price=min_price,
        max_price=max_price,
        min_quantity=min_quantity,
        max_quantity=max_quantity,
        offset=offset,
        limit=page_size,
    )


@router.get(
    "/inventory/{item_id}",
    response_model=InventoryResponse,
)
def get_inventory_item(
    item_id: UUID,
    current_user=Depends(get_current_user),
    inventory_service: InventoryService = Depends(get_inventory_service),
):
    return inventory_service.get_item(
        user_id=current_user.id,
        item_id=item_id,
    )


@router.put(
    "/inventory/{item_id}",
    dependencies=[Depends(validate_csrf)],
    response_model=InventoryResponse,
)
def update_inventory_item(
    item_id: UUID,
    data: InventoryUpdate,
    current_user=Depends(get_current_user),
    inventory_service: InventoryService = Depends(get_inventory_service),
):
    return inventory_service.update_item(
        user_id=current_user.id,
        item_id=item_id,
        data=data,
    )


@router.delete(
    "/inventory/{item_id}",
    dependencies=[Depends(validate_csrf)],
)
def delete_inventory_item(
    item_id: UUID,
    current_user=Depends(get_current_user),
    inventory_service: InventoryService = Depends(get_inventory_service),
):
    inventory_service.delete_item(
        user_id=current_user.id,
        item_id=item_id,
    )

    return {"detail": "Inventory item deleted"}


@router.patch(
    "/inventory/{item_id}/stock",
    dependencies=[Depends(validate_csrf)],
    response_model=InventoryResponse,
)
def adjust_inventory_stock(
    item_id: UUID,
    data: StockAdjustment,
    current_user=Depends(get_current_user),
    inventory_service: InventoryService = Depends(get_inventory_service),
):
    if data.operation == "in":
        return inventory_service.stock_in(
            user_id=current_user.id,
            item_id=item_id,
            quantity=data.quantity,
        )

    return inventory_service.stock_out(
        user_id=current_user.id,
        item_id=item_id,
        quantity=data.quantity,
    )


@router.get(
    "/dashboard/summary",
    response_model=InventoryDashboardSummary,
)
def get_dashboard_summary(
    current_user=Depends(get_current_user),
    inventory_service: InventoryService = Depends(get_inventory_service),
):
    total_items, total_quantity, total_inventory_value = (
        inventory_service.get_dashboard_summary(
            user_id=current_user.id,
        )
    )

    return InventoryDashboardSummary(
        total_items=total_items,
        total_quantity=total_quantity,
        total_inventory_value=total_inventory_value,
    )