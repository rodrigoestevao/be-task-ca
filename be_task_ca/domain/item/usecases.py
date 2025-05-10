"""This module contains the use cases for item-related operations.

Use cases encapsulate the business logic of the application, orchestrating
interactions between entities, repositories, and other services to achieve
specific outcomes. They are typically called by API handlers or other
service layers.
"""

from uuid import uuid4

from be_task_ca.domain.item.entities import Item
from be_task_ca.domain.item.schema import (
    AllItemsResponse,
    CreateItemRequest,
    CreateItemResponse,
)
from be_task_ca.interfaces.item import ItemRepository


class CreateItemUseCase:
    """Use case for creating a new item.

    This class handles the business logic required to create an item,
    including checking for duplicates by name and persisting the new item
    via the item repository.
    """

    def __init__(self, item_repository: ItemRepository) -> None:
        self.item_repository = item_repository

    def execute(self, request: CreateItemRequest) -> CreateItemResponse:
        """Executes the item creation process.

        It first checks if an item with the given name already exists. If so,
        it raises a ValueError. Otherwise, it creates a new Item entity,
        assigns a new UUID, saves it using the repository, and then returns
        the details of the created item.

        Args:
            request: A CreateItemRequest object containing the data for the new item.

        Raises:
            ValueError: If an item with the same name already exists.

        Returns:
            A CreateItemResponse object with the details of the newly created item,
            including its generated ID.
        """
        if self.item_repository.find_by_name(request.name):
            raise ValueError("An item with this name already exists")

        item = Item(
            id=uuid4(),
            name=request.name,
            description=request.description,
            price=request.price,
            quantity=request.quantity,
        )
        saved_item = self.item_repository.save(item)
        return CreateItemResponse(
            id=saved_item.id,
            name=saved_item.name,
            description=saved_item.description,
            price=saved_item.price,
            quantity=saved_item.quantity,
        )


class GetAllItemsUseCase:
    """Use case for retrieving all available items.

    This class handles the business logic for fetching all items
    from the repository and preparing them for presentation, typically
    as a list in a response schema.
    """

    def __init__(self, item_repository: ItemRepository) -> None:
        self.item_repository = item_repository

    def execute(self) -> AllItemsResponse:
        """Executes the process of retrieving all items.

        Fetches all items from the repository and formats them into an AllItemsResponse.

        Returns:
            An AllItemsResponse object containing a list of all items, where each item
            is represented as a CreateItemResponse.
        """
        items = self.item_repository.get_all()
        return AllItemsResponse(
            items=[
                CreateItemResponse(
                    id=item.id,
                    name=item.name,
                    description=item.description,
                    price=item.price,
                    quantity=item.quantity,
                )
                for item in items
            ]
        )
