"""
This module defines the core entities for the user domain.

These entities are simple data classes representing the structure of
user-related data within the application, independent of the database
or API layers.
"""
from dataclasses import dataclass
from uuid import UUID

@dataclass
class User:
    """Represents a user in the system.

    Attributes:
        id: The unique identifier for the user.
        email: The user's email address (must be unique).
        first_name: The user's first name.
        last_name: The user's last name.
        hashed_password: The user's password, hashed for security.
        shipping_address: The user's shipping address (optional).
        cart_items: A list of CartItem objects associated with this user.
    """
    id: UUID
    email: str
    first_name: str
    last_name: str
    hashed_password: str
    shipping_address: str | None
    cart_items: list["CartItem"]


@dataclass
class CartItem:
    """Represents an item within a user's shopping cart.

    Attributes:
        user_id: The unique identifier of the user who owns this cart item.
        item_id: The unique identifier of the item in the cart.
        quantity: The number of units of this item in the cart.
    """
    user_id: UUID
    item_id: UUID
    quantity: int
