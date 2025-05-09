from dataclasses import dataclass
from uuid import UUID, uuid4
from sqlalchemy.orm import Mapped, mapped_column
from be_task_ca.database import Base
from decimal import Decimal

@dataclass
class ItemModel(Base):
    __tablename__ = "items"

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4(),
        index=True,
    )
    name: Mapped[str] = mapped_column(unique=True, index=True)
    description: Mapped[str] = mapped_column(default=None)
    price: Mapped[Decimal] = mapped_column(default=None)
    quantity: Mapped[int] = mapped_column(default=0)
