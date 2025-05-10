"""This module provides an in-memory implementation of the UserRepository interface.

It's primarily used for testing or development environments where a persistent
database is not required. User and cart item data is stored in Python dictionaries
and lists in memory.
"""

from uuid import UUID

from be_task_ca.domain.user.entities import CartItem, User
from be_task_ca.interfaces.user import UserRepository


class InMemoryUserRepository(UserRepository):
    """An in-memory repository for User entities.

    This class implements the UserRepository interface, storing user data
    in a dictionary in memory. It's suitable for testing or scenarios
    where data persistence across sessions is not needed.
    """

    def __init__(self) -> None:
        self._users: dict[UUID, User] = {}

    def save(self, user: User) -> User:
        """Saves a user to the in-memory store.

        A deep copy of the user and its cart items is created to ensure
        that modifications to the input object outside this repository
        do not affect the stored version.

        Args:
            user: The User entity to save.

        Returns:
            The saved User entity (a deep copy of the input).
        """
        # Create a deep copy to avoid modifying the input
        cart_items = [
            CartItem(user_id=item.user_id, item_id=item.item_id, quantity=item.quantity)
            for item in user.cart_items
        ]
        saved_user = User(
            id=user.id,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            hashed_password=user.hashed_password,
            shipping_address=user.shipping_address,
            cart_items=cart_items,
        )
        self._users[user.id] = saved_user
        return saved_user

    def find_by_email(self, email: str) -> User | None:
        """Finds a user by their email address in the in-memory store.

        Args:
            email: The email address to search for.

        Returns:
            The User entity if found, otherwise None.
        """
        for user in self._users.values():
            if user.email == email:
                return user
        return None

    def find_by_id(self, user_id: UUID) -> User | None:
        """Finds a user by their unique ID in the in-memory store.

        Args:
            user_id: The UUID of the user to search for.

        Returns:
            The User entity if found, otherwise None.
        """
        return self._users.get(user_id)

    def find_cart_items(self, user_id: UUID) -> list[CartItem]:
        """Finds all cart items for a given user ID in the in-memory store.

        Args:
            user_id: The UUID of the user whose cart items are to be retrieved.

        Returns:
            A list of CartItem entities associated with the user.
            Returns an empty list if the user is not found or has no cart items.
        """
        user = self._users.get(user_id)
        return user.cart_items if user else []
