"""This module defines the Pydantic schemas for user-related API requests and responses.

These schemas are used for data validation, serialization, and documentation
of the API endpoints concerning users and their shopping carts.
"""

from uuid import UUID

from pydantic import BaseModel


class CreateUserRequest(BaseModel):
    """Schema for the request body when creating a new user."""

    first_name: str
    last_name: str
    email: str
    password: str
    shipping_address: str | None


class CreateUserResponse(BaseModel):
    """Schema for the response body after successfully creating a new user.

    Excludes sensitive information like the password.
    """

    id: UUID
    first_name: str
    last_name: str
    email: str
    shipping_address: str | None


class AddToCartRequest(BaseModel):
    """Schema for the request body when adding an item to a user's cart.

    Also used to represent an item within the AddToCartResponse.
    """

    item_id: UUID
    quantity: int


class AddToCartResponse(BaseModel):
    """Schema for the response body representing the contents of a user's cart."""

    items: list[AddToCartRequest]
