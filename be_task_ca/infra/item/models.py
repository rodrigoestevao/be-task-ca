"""This module defines the SQLAlchemy model for items.

SQLAlchemy models are Python classes that map to database tables.
This model represents the structure of the 'items' table in the database.
"""

from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID, uuid4

from sqlalchemy.orm import Mapped, mapped_column

from be_task_ca.infra.database import Base


@dataclass
class ItemModel(Base):
    """SQLAlchemy model representing an item in the 'items' table."""

    __tablename__ = "items"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4, index=True)
    name: Mapped[str] = mapped_column(unique=True, index=True)
    description: Mapped[str | None] = mapped_column(default=None)
    price: Mapped[Decimal] = mapped_column(default=0)
    quantity: Mapped[int] = mapped_column(default=0)
