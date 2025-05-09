from dataclasses import dataclass
from uuid import UUID
from decimal import Decimal


@dataclass
class Item:
    """Represents an item in the inventory or catalog.

    Attributes:
        id: The unique identifier for the item.
        name: The name of the item.
        description: An optional detailed description of the item.
        price: The price of the item.
        quantity: The available quantity of the item.
    """
    id: UUID
    name: str
    description: str | None
    price: Decimal
    quantity: int
