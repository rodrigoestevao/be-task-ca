"""Module for defining dependency injectors for user-related operations.

These functions are used by FastAPI's dependency injection system to provide
instances of use cases and database sessions to the API route handlers.
They handle the creation of necessary repositories and services, injecting
database sessions where needed.
"""

import os
from collections.abc import Iterator

from fastapi import Request

from be_task_ca.domain.user.usecases import (
    AddItemToCartUseCase,
    CreateUserUseCase,
    ListItemsInCartUseCase,
)
from be_task_ca.infra.database import SessionLocal
from be_task_ca.infra.user.in_memory_repository import InMemoryUserRepository
from be_task_ca.infra.user.item_service import MockItemService
from be_task_ca.infra.user.sqlalchemy_repository import SQLAlchemyUserRepository
from be_task_ca.interfaces.user import UserRepository


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


def get_user_repository(request: Request) -> UserRepository:
    """Returns the appropriate UserRepository based on environment configuration.

    Uses InMemoryUserRepository if REPOSITORY_TYPE is set to 'in_memory', otherwise
    uses SQLAlchemyUserRepository.
    """
    repository_type = os.getenv("REPOSITORY_TYPE", "sqlalchemy")
    if repository_type == "in_memory":
        return InMemoryUserRepository()
    return SQLAlchemyUserRepository(next(get_db(request)))


def get_create_user_use_case(request: Request) -> CreateUserUseCase:
    """Dependency to get an instance of CreateUserUseCase.

    Initializes the use case with a SQLAlchemyUserRepository, providing it
    with a database session obtained via the `get_db` generator.

    Args:
        request: The request object, used to get a database session.

    Returns:
        An instance of CreateUserUseCase.
    """
    return CreateUserUseCase(get_user_repository(request))


def get_add_item_to_cart_use_case(request: Request) -> AddItemToCartUseCase:
    """Dependency to get an instance of AddItemToCartUseCase.

    Initializes the use case with a SQLAlchemyUserRepository (which gets a
    database session via `get_db`) and a MockItemService.

    Args:
        request: The request object, used to get a database session.

    Returns:
        An instance of AddItemToCartUseCase.
    """
    return AddItemToCartUseCase(get_user_repository(request), MockItemService())


def get_list_all_items_in_cart_use_case(request: Request) -> ListItemsInCartUseCase:
    """Dependency to get an instance of ListItemsInCartUseCase.

    Initializes the use case with a SQLAlchemyUserRepository, providing it
    with a database session obtained via the `get_db` generator.

    Args:
        request: The request object, used to get a database session.

    Returns:
        An instance of ListItemsInCartUseCase.
    """
    return ListItemsInCartUseCase(get_user_repository(request))
