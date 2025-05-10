"""This module defines the Pydantic schemas for item-related API requests and responses.

Pydantic models are used for data validation and serialization/deserialization
in FastAPI applications. These schemas ensure that data exchanged with the
item API endpoints conforms to the expected structure and types.
"""

from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel


class CreateItemRequest(BaseModel):
    """Schema for the request body when creating a new item."""

    name: str
    description: str | None = None
    price: Decimal
    quantity: int


class CreateItemResponse(CreateItemRequest):
    """Schema for the response body after successfully creating an item.

    Inherits all fields from CreateItemRequest and adds the item's unique ID.
    """

    id: UUID


class AllItemsResponse(BaseModel):
    """Schema for the response body when retrieving a list of all items."""

    items: list[CreateItemResponse]
