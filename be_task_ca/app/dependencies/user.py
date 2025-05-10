"""Module for defining dependency injectors for user-related operations.

These functions are used by FastAPI's dependency injection system to provide
instances of use cases and database sessions to the API route handlers.
They handle the creation of necessary repositories and services, injecting
database sessions where needed.
"""

from collections.abc import Iterator

from fastapi import Request

from be_task_ca.domain.user.usecases import (
    AddItemToCartUseCase,
    CreateUserUseCase,
    ListItemsInCartUseCase,
)
from be_task_ca.infra.database import SessionLocal
from be_task_ca.infra.user.item_service import MockItemService
from be_task_ca.infra.user.sqlalchemy_repository import SQLAlchemyUserRepository


def get_db(request: Request) -> Iterator:  # noqa: ARG001
    """Provides a database session as a context-managed generator.

    This function creates a new SQLAlchemy session for a request and ensures
    it's closed afterwards. It's designed to be used as a generator,
    typically with `next()` to retrieve the session.

    Args:
        request: The request object. Currently unused but included
                 for consistency with dependency patterns.

    Yields:
        sqlalchemy.orm.Session: The database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_create_user_use_case(request: Request) -> CreateUserUseCase:
    """Dependency to get an instance of CreateUserUseCase.

    Initializes the use case with a SQLAlchemyUserRepository, providing it
    with a database session obtained via the `get_db` generator.

    Args:
        request: The request object, used to get a database session.

    Returns:
        An instance of CreateUserUseCase.
    """
    return CreateUserUseCase(SQLAlchemyUserRepository(next(get_db(request))))


def get_add_item_to_cart_use_case(request: Request) -> AddItemToCartUseCase:
    """Dependency to get an instance of AddItemToCartUseCase.

    Initializes the use case with a SQLAlchemyUserRepository (which gets a
    database session via `get_db`) and a MockItemService.

    Args:
        request: The request object, used to get a database session.

    Returns:
        An instance of AddItemToCartUseCase.
    """
    return AddItemToCartUseCase(
        SQLAlchemyUserRepository(next(get_db(request))), MockItemService()
    )


def get_list_all_items_in_cart_use_case(request: Request) -> ListItemsInCartUseCase:
    """Dependency to get an instance of ListItemsInCartUseCase.

    Initializes the use case with a SQLAlchemyUserRepository, providing it
    with a database session obtained via the `get_db` generator.

    Args:
        request: The request object, used to get a database session.

    Returns:
        An instance of ListItemsInCartUseCase.
    """
    return ListItemsInCartUseCase(SQLAlchemyUserRepository(next(get_db(request))))
