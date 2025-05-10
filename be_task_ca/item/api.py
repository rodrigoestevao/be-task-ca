"""This module defines the API endpoints for item-related operations.

It uses FastAPI to create routes for creating and retrieving items,
leveraging use cases for business logic and dependency injection for
repository access.
"""

from fastapi import APIRouter, Depends, HTTPException, status

from be_task_ca.dependencies import (
    get_create_item_use_case,
    get_list_all_items_in_cart_use_case,
)
from be_task_ca.item.schema import (
    AllItemsResponse,
    CreateItemRequest,
    CreateItemResponse,
)
from be_task_ca.item.usecases import CreateItemUseCase, GetAllItemsUseCase

item_router = APIRouter(prefix="/items", tags=["item"])


@item_router.post("/", response_model=CreateItemResponse)
async def post_item(
    item: CreateItemRequest,
    use_case: CreateItemUseCase = Depends(get_create_item_use_case),
) -> CreateItemResponse:
    """Creates a new item.

    Receives item data, passes it to the CreateItemUseCase, and returns
    the created item's details.

    Args:
        item: The request body containing the details of the item to create.
        use_case: The injected use case for creating an item.

    Raises:
        HTTPException: 409 Conflict if an item with the same name already exists.

    Returns:
        The details of the newly created item.
    """
    try:
        response = use_case.execute(item)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e)) from e
    return response


@item_router.get("/", response_model=AllItemsResponse)
async def get_items(
    use_case: GetAllItemsUseCase = Depends(get_list_all_items_in_cart_use_case),
) -> AllItemsResponse:
    """Retrieves all available items.

    Args:
        use_case: The injected use case for retrieving all items.

    Returns:
        A list of all items.
    """
    return use_case.execute()
