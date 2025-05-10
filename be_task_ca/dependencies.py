"""Module for defining FastAPI dependency injectors.

These functions are used by FastAPI's dependency injection system to provide
instances of use cases to the API route handlers. They handle the creation
of necessary repositories and services, injecting database sessions where needed.
"""

from fastapi import Request

from be_task_ca.common import get_db
from be_task_ca.item.infra.sqlalchemy_repository import SQLAlchemyItemRepository
from be_task_ca.item.usecases import CreateItemUseCase, GetAllItemsUseCase
from be_task_ca.user.infra.item_service import MockItemService
from be_task_ca.user.infra.sqlalchemy_repository import SQLAlchemyUserRepository
from be_task_ca.user.usecases import (
    AddItemToCartUseCase,
    CreateUserUseCase,
    ListItemsInCartUseCase,
)


def get_create_item_use_case(request: Request) -> CreateItemUseCase:
    """Dependency to get an instance of CreateItemUseCase.

    Initializes the use case with a SQLAlchemyItemRepository, providing it
    with a database session obtained from the request.

    Args:
        request: The request object, used to get a database session.

    Returns:
        An instance of CreateItemUseCase.
    """
    return CreateItemUseCase(SQLAlchemyItemRepository(next(get_db(request))))


def get_all_items_use_case(request: Request) -> GetAllItemsUseCase:
    """Dependency to get an instance of GetAllItemsUseCase.

    Initializes the use case with a SQLAlchemyItemRepository, providing it
    with a database session obtained from the request.

    Args:
        request: The request object, used to get a database session.

    Returns:
        An instance of GetAllItemsUseCase.
    """
    return GetAllItemsUseCase(SQLAlchemyItemRepository(next(get_db(request))))


def get_create_user_use_case(request: Request) -> CreateUserUseCase:
    """Dependency to get an instance of CreateUserUseCase.

    Initializes the use case with a SQLAlchemyUserRepository, providing it
    with a database session obtained from the request.

    Args:
        request: The request object, used to get a database session.

    Returns:
        An instance of CreateUserUseCase.
    """
    return CreateUserUseCase(SQLAlchemyUserRepository(next(get_db(request))))


def get_add_item_to_cart_use_case(request: Request) -> AddItemToCartUseCase:
    """Dependency to get an instance of AddItemToCartUseCase.

    Initializes the use case with a SQLAlchemyUserRepository (with a database session)
    and a MockItemService.

    Args:
        request: The request object, used to get a database session for the repository.

    Returns:
        An instance of AddItemToCartUseCase.
    """
    return AddItemToCartUseCase(
        SQLAlchemyUserRepository(next(get_db(request))), MockItemService()
    )


def get_list_all_items_in_cart_use_case(request: Request) -> ListItemsInCartUseCase:
    """Dependency to get an instance of ListItemsInCartUseCase.

    Initializes the use case with a SQLAlchemyUserRepository, providing it
    with a database session obtained from the request.

    Args:
        request: The request object, used to get a database session.

    Returns:
        An instance of ListItemsInCartUseCase.
    """
    return ListItemsInCartUseCase(SQLAlchemyUserRepository(next(get_db(request))))
