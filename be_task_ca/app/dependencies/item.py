"""Module for defining dependency injectors for item-related operations.

These functions are used by FastAPI's dependency injection system to provide
instances of use cases and database sessions to the API route handlers.
They handle the creation of necessary repositories, injecting
database sessions where needed.
"""

from collections.abc import Iterator

from fastapi import Request

from be_task_ca.domain.item.usecases import CreateItemUseCase, GetAllItemsUseCase
from be_task_ca.infra.database import SessionLocal
from be_task_ca.infra.item.sqlalchemy_repository import SQLAlchemyItemRepository


def get_db(request: Request) -> Iterator:  # noqa: ARG001
    """Provides a database session as a context-managed generator.

    This function creates a new SQLAlchemy session for a request and ensures
    it's closed afterwards. It's designed to be used as a generator,
    typically with `next()` to retrieve the session.

    Args:
        request: The request object. Currently unused but included for
        consistency with dependency patterns.

    Yields:
        sqlalchemy.orm.Session: The database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_create_item_use_case(request: Request) -> CreateItemUseCase:
    """Dependency to get an instance of CreateItemUseCase.

    Initializes the use case with a SQLAlchemyItemRepository, providing it
    with a database session obtained via the `get_db` generator.

    Args:
        request: The request object, used to get a database session.

    Returns:
        An instance of CreateItemUseCase.
    """
    return CreateItemUseCase(SQLAlchemyItemRepository(next(get_db(request))))


def get_all_items_use_case(request: Request) -> GetAllItemsUseCase:
    """Dependency to get an instance of GetAllItemsUseCase.

    Initializes the use case with a SQLAlchemyItemRepository, providing it
    with a database session obtained via the `get_db` generator.

    Args:
        request: The request object, used to get a database session.

    Returns:
        An instance of GetAllItemsUseCase.
    """
    return GetAllItemsUseCase(SQLAlchemyItemRepository(next(get_db(request))))
