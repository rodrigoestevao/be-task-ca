"""This module provides the SQLAlchemy implementation of the ItemRepository interface.

It handles the persistence and retrieval of Item entities using SQLAlchemy
to interact with a relational database.
"""

from uuid import UUID

from sqlalchemy.orm import Session

from be_task_ca.domain.item.entities import Item
from be_task_ca.infra.item.models import ItemModel
from be_task_ca.interfaces.item import ItemRepository


class SQLAlchemyItemRepository(ItemRepository):
    """A repository class for Item entities that uses SQLAlchemy for database operations.

    This class implements the ItemRepository interface, providing concrete methods
    to save, find, and retrieve items from a database via SQLAlchemy.
    """

    def __init__(self, db: Session) -> None:
        self.db = db

    def save(self, item: Item) -> Item:
        """Saves an item to the repository.

        If the item already exists (e.g., based on its ID), it should be updated.
        If it's a new item, it should be created.

        Args:
            item: The Item entity to save.

        Returns:
            The saved Item entity, potentially with updated fields (e.g., generated
            ID or timestamps).
        """
        db_item = ItemModel(
            id=item.id,
            name=item.name,
            description=item.description,
            price=item.price,
            quantity=item.quantity,
        )
        self.db.add(db_item)
        self.db.commit()
        return item

    def find_by_name(self, name: str) -> Item | None:
        """Finds an item by its name.

        Args:
            name: The name of the item to find.

        Returns:
            The Item entity if found, otherwise None.
        """
        db_item = self.db.query(ItemModel).filter(ItemModel.name == name).first()
        if db_item:
            return Item(
                id=db_item.id,
                name=db_item.name,
                description=db_item.description,
                price=db_item.price,
                quantity=db_item.quantity,
            )
        return None

    def find_by_id(self, id: UUID) -> Item | None:
        """Finds an item by its unique identifier.

        Args:
            id: The UUID of the item to find.

        Returns:
            The Item entity if found, otherwise None.
        """
        db_item = self.db.query(ItemModel).filter(ItemModel.id == id).first()
        if db_item:
            return Item(
                id=db_item.id,
                name=db_item.name,
                description=db_item.description,
                price=db_item.price,
                quantity=db_item.quantity,
            )
        return None

    def get_all(self) -> list[Item]:
        """Retrieves all items from the repository.

        Returns:
            A list of all Item entities.
        """
        db_items = self.db.query(ItemModel).all()
        return [
            Item(
                id=item.id,
                name=item.name,
                description=item.description,
                price=item.price,
                quantity=item.quantity,
            )
            for item in db_items
        ]
