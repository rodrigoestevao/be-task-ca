"""This module defines the interfaces for item-related operations.

Interfaces, also known as abstract base classes (ABCs) in Python,
define a contract that concrete classes must implement. This promotes
loose coupling and testability.
"""

import abc
from uuid import UUID

from be_task_ca.domain.item.entities import Item


class ItemRepository(abc.ABC):
    """Abstract base class defining the contract for item data persistence.

    This interface outlines the methods that any concrete item repository
    implementation (e.g., for a specific database) must provide.
    """

    @abc.abstractmethod
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
        raise NotImplementedError

    @abc.abstractmethod
    def find_by_name(self, name: str) -> Item | None:
        """Finds an item by its name.

        Args:
            name: The name of the item to find.

        Returns:
            The Item entity if found, otherwise None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def find_by_id(self, id: UUID) -> Item | None:
        """Finds an item by its unique identifier.

        Args:
            id: The UUID of the item to find.

        Returns:
            The Item entity if found, otherwise None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_all(self) -> list[Item]:
        """Retrieves all items from the repository.

        Returns:
            A list of all Item entities.
        """
        raise NotImplementedError
