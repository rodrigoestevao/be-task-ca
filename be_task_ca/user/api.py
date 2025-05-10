"""This module defines the API endpoints for user-related operations.

It uses FastAPI to create routes for creating users, adding items to their cart,
and retrieving cart contents. It leverages use cases for business logic and
dependency injection for repository and service access.
"""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from be_task_ca.dependencies import (
    get_add_item_to_cart_use_case,
    get_create_user_use_case,
    get_list_all_items_in_cart_use_case,
)
from be_task_ca.user.schema import (
    AddToCartRequest,
    AddToCartResponse,
    CreateUserRequest,
    CreateUserResponse,
)
from be_task_ca.user.usecases import (
    AddItemToCartUseCase,
    CreateUserUseCase,
    ListItemsInCartUseCase,
)

user_router = APIRouter(prefix="/users", tags=["user"])


@user_router.post("/")
async def post_customer(
    user: CreateUserRequest,
    use_case: CreateUserUseCase = Depends(get_create_user_use_case),
) -> CreateUserResponse:
    """Creates a new user.

    Receives user data, passes it to the CreateUserUseCase, and returns
    the created user's details.

    Args:
        user: The request body containing the details of the user to create.
        use_case: The injected use case for creating a user.

    Raises:
        HTTPException: 409 Conflict if a user with the same email already exists.

    Returns:
        The details of the newly created user.
    """
    try:
        response = use_case.execute(user)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e)) from e
    return response


@user_router.post("/{user_id}/cart")
async def post_cart(
    user_id: UUID,
    cart_item: AddToCartRequest,
    use_case: AddItemToCartUseCase = Depends(get_add_item_to_cart_use_case),
) -> AddToCartResponse:
    """Adds an item to a specific user's shopping cart.

    Args:
        user_id: The unique identifier of the user.
        cart_item: The request body containing the item ID and quantity to add.
        use_case: The injected use case for adding an item to the cart.

    Raises:
        HTTPException: 409 Conflict if the user does not exist,
                       the item does not exist, there's not enough stock,
                       or the item is already in the cart.
                       (Note: The specific status code might vary based on the
                       nature of the ValueError raised by the use case,
                       currently it's a generic 409).

    Returns:
        The updated list of items in the user's cart.
    """
    try:
        response = await use_case.execute(user_id, cart_item)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e)) from e
    return response


@user_router.get("/{user_id}/cart")
async def get_cart(
    user_id: UUID,
    use_case: ListItemsInCartUseCase = Depends(get_list_all_items_in_cart_use_case),
) -> AddToCartResponse:
    """Retrieves all items in a specific user's shopping cart.

    Args:
        user_id: The unique identifier of the user whose cart is to be retrieved.
        use_case: The injected use case for listing items in the cart.

    Returns:
        A list of items currently in the user's cart.
        Returns an empty list if the cart is empty or the user does not exist.
    """
    return use_case.execute(user_id)
