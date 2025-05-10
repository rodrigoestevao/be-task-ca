"""This module defines the SQLAlchemy models for user-related data.

SQLAlchemy models are Python classes that map to database tables.
These models represent the structure of the 'users' and 'cart_items' tables.
"""

from dataclasses import dataclass
from uuid import UUID, uuid4

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from be_task_ca.database import Base


@dataclass
class UserModel(Base):
    """SQLAlchemy model representing a user in the 'users' table.

    Attributes:
        id: The primary key for the user, a UUID.
        email: The user's email address, must be unique.
        first_name: The user's first name.
        last_name: The user's last name.
        hashed_password: The user's password, hashed for security.
        shipping_address: The user's shipping address (optional).
        cart_items: A relationship to the CartItemModel, representing
                    the items in the user's shopping cart.
    """

    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4, index=True)
    email: Mapped[str] = mapped_column(unique=True, index=True)
    first_name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str] = mapped_column(nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    shipping_address: Mapped[str | None] = mapped_column(default=None)
    cart_items: Mapped[list["CartItemModel"]] = relationship()


@dataclass
class CartItemModel(Base):
    """SQLAlchemy model representing an item in a user's shopping cart.

    This table acts as a join table between users and items, also storing
    the quantity of each item in a specific user's cart.
    """

    __tablename__ = "cart_items"

    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), primary_key=True)
    item_id: Mapped[UUID] = mapped_column(ForeignKey("items.id"), primary_key=True)
    quantity: Mapped[int] = mapped_column(default=0)
