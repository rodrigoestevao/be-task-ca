"""This module defines the core entities for the item domain.

These entities are simple data classes representing the structure of
item-related data within the application, independent of the database
or API layers.
"""

from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID


@dataclass
class Item:
    """Represents an item in the inventory or catalog."""

    id: UUID
    name: str
    description: str | None
    price: Decimal
    quantity: int

    def __post_init__(self) -> None:
        if self.price < Decimal("0"):
            raise ValueError("Price cannot be negative")

        if self.quantity < 0:
            raise ValueError("Quantity cannot be negative")
