"""This module defines the interfaces for user-related data persistence.

Interfaces, also known as abstract base classes (ABCs) in Python,
define a contract that concrete classes must implement. This promotes
loose coupling and testability within the user domain.
"""

import abc
from uuid import UUID

from be_task_ca.domain.user.entities import CartItem, User


class UserRepository(abc.ABC):
    """Abstract base class defining the contract for user data persistence.

    This interface outlines the methods that any concrete user repository
    implementation (e.g., for a specific database) must provide.
    """

    @abc.abstractmethod
    def save(self, user: User) -> User:
        """Saves a user to the repository.

        If the user already exists (e.g., based on their ID), they should be updated.
        If it's a new user, they should be created.

        Args:
            user: The User entity to save.

        Returns:
            The saved User entity, potentially with updated fields (e.g., generated ID
            or timestamps).
        """
        raise NotImplementedError

    @abc.abstractmethod
    def find_by_email(self, email: str) -> User | None:
        """Finds a user by their email address.

        Args:
            email: The email address of the user to find.

        Returns:
            The User entity if found, otherwise None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def find_by_id(self, user_id: UUID) -> User | None:
        """Finds a user by their unique identifier.

        Args:
            user_id: The UUID of the user to find.

        Returns:
            The User entity if found, otherwise None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def find_cart_items(self, user_id: UUID) -> list[CartItem]:
        """Retrieves all cart items associated with a specific user.

        Args:
            user_id: The unique identifier of the user whose cart items are to
                be retrieved.

        Returns:
            A list of CartItem entities. Returns an empty list if the user has
            no cart items or does not exist.
        """
        raise NotImplementedError


class ItemService(abc.ABC):
    """Abstract base class defining the contract for item-related business logic.

    This interface outlines methods that an item service implementation
    would provide, often interacting with an ItemRepository or other services.
    """

    @abc.abstractmethod
    async def get_item(self, item_id: UUID) -> dict | None:
        """Retrieves detailed information about a specific item.

        The exact structure of the returned dictionary may vary depending
        on the implementation but should contain relevant item details.

        Args:
            item_id: The unique identifier of the item to retrieve.

        Returns:
            A dictionary containing item details if found, otherwise None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    async def check_stock(self, item_id: UUID, quantity: int) -> bool:
        """Checks if a sufficient quantity of an item is available in stock.

        Args:
            item_id: The unique identifier of the item to check.
            quantity: The desired quantity to check against the stock.

        Returns:
            True if the item exists and the requested quantity is available,
            False otherwise.
        """
        raise NotImplementedError
