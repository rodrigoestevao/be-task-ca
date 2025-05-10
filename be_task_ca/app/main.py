"""Main application setup and route definitions.

This module initializes the FastAPI application and includes routers for user
and item operations.
"""

from uuid import UUID

from fastapi import APIRouter, Depends, FastAPI, HTTPException, status

from be_task_ca.app.dependencies.item import (
    get_all_items_use_case,
    get_create_item_use_case,
)
from be_task_ca.app.dependencies.user import (
    get_add_item_to_cart_use_case,
    get_create_user_use_case,
    get_list_all_items_in_cart_use_case,
)
from be_task_ca.domain.item.schema import (
    AllItemsResponse,
    CreateItemRequest,
    CreateItemResponse,
)
from be_task_ca.domain.item.usecases import CreateItemUseCase, GetAllItemsUseCase
from be_task_ca.domain.user.schema import (
    AddToCartRequest,
    AddToCartResponse,
    CreateUserRequest,
    CreateUserResponse,
)
from be_task_ca.domain.user.usecases import (
    AddItemToCartUseCase,
    CreateUserUseCase,
    ListItemsInCartUseCase,
)

app = FastAPI()

# User Routes
user_router = APIRouter(prefix="/users", tags=["user"])


@user_router.post("/", response_model=CreateUserResponse)
async def post_customer(
    user: CreateUserRequest,
    use_case: CreateUserUseCase = Depends(get_create_user_use_case),
) -> CreateUserResponse:
    """Creates a new user.

    Args:
        user: The user data from the request body.
        use_case: The dependency-injected use case for creating a user.

    Raises:
        HTTPException: 409 Conflict if a user with the given email already exists.

    Returns:
        The created user's details.
    """
    try:
        response = use_case.execute(user)
    except ValueError as e:
        # Assuming ValueError from use_case indicates a duplicate email or similar conflict
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e)) from e
    return response


@user_router.post("/{user_id}/cart", response_model=AddToCartResponse)
async def post_cart(
    user_id: UUID,
    cart_item: AddToCartRequest,
    use_case: AddItemToCartUseCase = Depends(get_add_item_to_cart_use_case),
) -> AddToCartResponse:
    """Adds an item to a specified user's shopping cart.

    Args:
        user_id: The ID of the user whose cart is being modified.
        cart_item: The item and quantity to add to the cart.
        use_case: The dependency-injected use case for adding an item to a cart.

    Raises:
        HTTPException: 409 Conflict if the user or item does not exist,
                       or if there's an issue adding the item (e.g., insufficient stock,
                       though this specific use case uses a MockItemService).

    Returns:
        The updated cart contents.
    """
    try:
        response = await use_case.execute(user_id, cart_item)
    except ValueError as e:
        # Assuming ValueError from use_case indicates an issue like user/item not found
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e)) from e
    return response


@user_router.get("/{user_id}/cart", response_model=AddToCartResponse)
async def get_cart(
    user_id: UUID,
    use_case: ListItemsInCartUseCase = Depends(get_list_all_items_in_cart_use_case),
) -> AddToCartResponse:
    """Retrieves all items in a specified user's shopping cart.

    Args:
        user_id: The ID of the user whose cart is being retrieved.
        use_case: The dependency-injected use case for listing cart items.

    Returns:
        The contents of the user's cart.
    """
    return use_case.execute(user_id)


# Item Routes
item_router = APIRouter(prefix="/items", tags=["item"])


@item_router.post("/", response_model=CreateItemResponse)
async def post_item(
    item: CreateItemRequest,
    use_case: CreateItemUseCase = Depends(get_create_item_use_case),
) -> CreateItemResponse:
    """Creates a new item.

    Args:
        item: The item data from the request body.
        use_case: The dependency-injected use case for creating an item.

    Raises:
        HTTPException: 409 Conflict if an item with the given name already exists
                       or if there's a validation error (e.g., negative price).

    Returns:
        The created item's details.
    """
    try:
        response = use_case.execute(item)
    except ValueError as e:
        # Assuming ValueError from use_case indicates a duplicate name or validation issue
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e)) from e
    return response


@item_router.get("/", response_model=AllItemsResponse)
async def get_items(
    use_case: GetAllItemsUseCase = Depends(get_all_items_use_case),
) -> AllItemsResponse:
    """Retrieves all available items.

    Args:
        use_case: The dependency-injected use case for getting all items.

    Returns:
        A list of all items.
    """
    return use_case.execute()


# Root Endpoint
@app.get("/")
async def root() -> dict:
    """Root endpoint for the API.

    Returns:
        A simple greeting message.
    """
    return {"message": "Thanks for shopping at Nile!"}


app.include_router(user_router)
app.include_router(item_router)
