"""This module provides a mock implementation of the ItemService interface.

It's intended for use in development, testing, or when a real item service
is not available or not yet integrated, allowing other parts of the system
(like user use cases) to function without a live item service dependency.
"""
from uuid import UUID

from be_task_ca.user.interfaces import ItemService


class MockItemService(ItemService):
    """A mock implementation of the ItemService interface.

    This service simulates interactions with an item management system,
    returning predefined or simple mock data. It's useful for decoupling
    the user service from a concrete item service during development or testing.

    Note: The responses from this mock service are hardcoded and do not
    reflect a real inventory system.
    """
    async def get_item(self, item_id: UUID) -> dict | None:
        """Retrieves mock details for a given item ID.

        This is a mock implementation and always returns a predefined item
        structure, using the provided item_id in its response. In a real
        scenario, this would involve an API call or database lookup.

        Args:
            item_id: The UUID of the item to retrieve.

        Returns:
            A dictionary containing mock item details.
        """
        # Mock implementation; replace with actual API call in production
        return {
            "id": item_id, "name": "Mock Item", "quantity": 12,
        }

    async def check_stock(self, item_id: UUID, quantity: int) -> bool:
        """Checks if a mock item has sufficient stock based on its mock quantity.

        Args:
            item_id: The UUID of the item to check stock for.
            quantity: The desired quantity to check.

        Returns:
            True if the mock item's quantity is greater than or equal to the
            requested quantity, False otherwise.
        """
        # Mock implementation; replace with actual API call in production
        item = await self.get_item(item_id)
        return item is not None and item["quantity"] >= quantity
