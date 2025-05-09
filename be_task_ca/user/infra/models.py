from dataclasses import dataclass
from typing import List
import uuid

from sqlalchemy import UUID, ForeignKey
from be_task_ca.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship


@dataclass
class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4(),
        index=True,
    )
    email: Mapped[str] = mapped_column(unique=True, index=True)
    first_name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str] = mapped_column(nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    shipping_address: Mapped[str] = mapped_column(default=None)
    cart_items: Mapped[list["CartItemModel"]] = relationship()


@dataclass
class CartItemModel(Base):
    __tablename__ = "cart_items"

    # user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), primary_key=True, index=True)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), primary_key=True)
    item_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("items.id"), primary_key=True)
    quantity: Mapped[int] = mapped_column(default=0)
