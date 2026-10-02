class InventoryError(Exception):
    """Base exception for inventory-related errors."""


class InventoryNotFoundError(InventoryError):
    """Raised when an inventory item cannot be found."""


class DuplicateSKUError(InventoryError):
    """Raised when a user attempts to create a duplicate SKU."""


class DuplicateItemNameError(InventoryError):
    """Raised when a user attempts to create a duplicate item name."""


class InvalidStockAdjustmentError(InventoryError):
    """Raised when a stock adjustment is invalid."""