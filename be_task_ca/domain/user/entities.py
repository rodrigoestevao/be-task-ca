"""This module defines the core entities for the user domain.

These entities are simple data classes representing the structure of
user-related data within the application, independent of the database
or API layers.
"""

from dataclasses import asdict, dataclass
from uuid import UUID


@dataclass
class CartItem:
    """Represents an item within a user's shopping cart."""

    user_id: UUID
    item_id: UUID
    quantity: int

    def __post_init__(self) -> None:
        if self.quantity <= 0:
            raise ValueError("Quantity must be positive")

    def model_dump(self) -> dict:
        """Converts the CartItem dataclass instance to a dictionary.

        Returns:
            A dictionary representation of the CartItem instance.
        """
        return asdict(self)


@dataclass
class User:
    """Represents a user in the system."""

    id: UUID
    email: str
    first_name: str
    last_name: str
    hashed_password: str
    shipping_address: str | None
    cart_items: list["CartItem"]

    def model_dump(self) -> dict:
        """Converts the User dataclass instance to a dictionary.

        Returns:
            A dictionary representation of the User instance.
        """
        return asdict(self)
