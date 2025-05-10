"""This module contains the use cases for user-related operations.

Use cases encapsulate the business logic of the application, orchestrating
interactions between entities, repositories, and other services to achieve
specific outcomes related to users and their carts.
"""

import hashlib
from uuid import UUID, uuid4

from be_task_ca.domain.user.entities import CartItem, User
from be_task_ca.domain.user.schema import (
    AddToCartRequest,
    AddToCartResponse,
    CreateUserRequest,
    CreateUserResponse,
)
from be_task_ca.interfaces.user import ItemService, UserRepository


class CreateUserUseCase:
    """Use case for creating a new user.

    This class handles the business logic required to create a user,
    including checking for existing users with the same email, hashing
    the password, and persisting the new user.
    """

    def __init__(self, user_repository: UserRepository) -> None:
        self.user_repository = user_repository

    def execute(self, request: CreateUserRequest) -> CreateUserResponse:
        """Executes the user creation process.

        Checks if a user with the given email already exists. If not,
        it creates a new User entity, hashes the password, saves it
        through the repository, and returns the details of the created user.

        Args:
            request: A CreateUserRequest object containing the data for the new user.

        Raises:
            ValueError: If a user with the same email address already exists.

        Returns:
            A CreateUserResponse object with the details of the newly created user.
        """
        if self.user_repository.find_by_email(request.email):
            raise ValueError("An user with this email already exists")
        user = User(
            id=uuid4(),
            first_name=request.first_name,
            last_name=request.last_name,
            email=request.email,
            hashed_password=hashlib.sha512(
                request.password.encode("utf-8")
            ).hexdigest(),
            shipping_address=request.shipping_address,
            cart_items=[],
        )
        saved_user = self.user_repository.save(user)
        return CreateUserResponse(**saved_user.model_dump())


class AddItemToCartUseCase:
    """Use case for adding an item to a user's shopping cart.

    This class handles the business logic for adding an item to a cart,
    including validating the user and item, checking item stock, ensuring
    the item isn't already in the cart, and then saving the updated cart.
    """

    def __init__(
        self, user_repository: UserRepository, item_service: ItemService
    ) -> None:
        self.user_repository = user_repository
        self.item_service = item_service

    async def execute(
        self, user_id: UUID, request: AddToCartRequest
    ) -> AddToCartResponse:
        """Executes the process of adding an item to a user's cart.

        Validations performed:
        - Checks if the user exists.
        - Checks if the item exists using the item_service.
        - Checks if there is enough stock for the item using the item_service.
        - Checks if the item is already present in the user's cart.

        If all validations pass, the item is added to the user's cart,
        the user entity is saved, and the updated cart contents are returned.

        Args:
            user_id: The ID of the user to whose cart the item will be added.
            request: An AddToCartRequest object containing the item ID and quantity.

        Raises:
            ValueError: If the user does not exist, item does not exist, not enough stock,
                        or item is already in the cart.

        Returns:
            An AddToCartResponse object representing the current state of the user's cart.
        """
        user = self.user_repository.find_by_id(user_id)
        if not user:
            raise ValueError("User does not exists")
        item = await self.item_service.get_item(request.item_id)
        if not item:
            raise ValueError("Item does not exists")
        if not await self.item_service.check_stock(
            request.item_id, quantity=request.quantity
        ):
            raise ValueError("Not enough items in stock")
        if any(cart_item.item_id == request.item_id for cart_item in user.cart_items):
            raise ValueError("Item already in cart")
        cart_item = CartItem(
            user_id=user_id, item_id=request.item_id, quantity=request.quantity
        )
        user.cart_items.append(cart_item)
        self.user_repository.save(user)
        return AddToCartResponse(
            items=[
                AddToCartRequest(item_id=cart_item.item_id, quantity=cart_item.quantity)
                for cart_item in user.cart_items
            ]
        )


class ListItemsInCartUseCase:
    """Use case for listing all items in a user's shopping cart.

    This class handles the business logic for retrieving and presenting
    the items currently in a specified user's cart.
    """

    def __init__(self, user_repository: UserRepository) -> None:
        self.user_repository = user_repository

    def execute(self, user_id: UUID) -> AddToCartResponse:
        """Executes the process of listing items in a user's cart.

        Args:
            user_id: The ID of the user whose cart items are to be listed.

        Returns:
            An AddToCartResponse object containing a list of items in the user's
            cart.
        """
        cart_items = self.user_repository.find_cart_items(user_id)
        return AddToCartResponse(
            items=[
                AddToCartRequest(item_id=cart_item.item_id, quantity=cart_item.quantity)
                for cart_item in cart_items
            ]
        )
