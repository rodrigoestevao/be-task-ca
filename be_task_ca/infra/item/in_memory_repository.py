"""This module provides an in-memory implementation of the ItemRepository interface.

It's primarily used for testing or development environments where a persistent
database is not required. Item data is stored in a Python dictionary in memory.
"""

from uuid import UUID

from be_task_ca.domain.item.entities import Item
from be_task_ca.interfaces.item import ItemRepository


class InMemoryItemRepository(ItemRepository):
    """An in-memory repository for Item entities.

    This class implements the ItemRepository interface, storing item data
    in a dictionary in memory. It's suitable for testing or scenarios
    where data persistence across sessions is not needed.
    """

    def __init__(self) -> None:
        self._items: dict[UUID, Item] = {}

    def save(self, item: Item) -> Item:
        """Saves an item to the in-memory store.

        A copy of the item is created to ensure that modifications
        to the input object outside this repository do not affect the stored version.

        Args:
            item: The Item entity to save.

        Returns:
            The saved Item entity (a copy of the input).
        """
        # Create a copy to avoid modifying the input
        saved_item = Item(
            id=item.id,
            name=item.name,
            description=item.description,
            price=item.price,
            quantity=item.quantity,
        )
        self._items[item.id] = saved_item
        return saved_item

    def find_by_id(self, item_id: UUID) -> Item | None:
        """Finds an item by its unique ID in the in-memory store.

        Args:
            item_id: The UUID of the item to search for.

        Returns:
            The Item entity if found, otherwise None.
        """
        return self._items.get(item_id)

    def find_by_name(self, name: str) -> Item | None:
        """Finds an item by its name in the in-memory store.

        Args:
            name: The name of the item to find.

        Returns:
            The Item entity if found, otherwise None.
        """
        for item in self._items.values():
            if item.name == name:
                return item
        return None

    def get_all(self) -> list[Item]:
        """Retrieves all items from the in-memory store.

        Returns:
            A list of all Item entities currently stored.
        """
        return list(self._items.values())
