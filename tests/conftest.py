"""This module defines shared Pytest fixtures for the test suite.

Fixtures defined here are automatically available to all tests in the
`tests` directory and its subdirectories. These fixtures primarily provide
mocked versions of repository and service interfaces for dependency injection
during testing.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock
from sqlalchemy.orm import Session
from be_task_ca.item.interfaces import ItemRepository
from be_task_ca.user.interfaces import UserRepository, ItemService


@pytest.fixture
def mock_item_repository() -> MagicMock:
    """Pytest fixture that provides a mock ItemRepository.

    Returns:
        A MagicMock instance configured to spec ItemRepository.
    """
    return MagicMock(spec=ItemRepository)


@pytest.fixture
def mock_user_repository() -> MagicMock:
    """Pytest fixture that provides a mock UserRepository.

    Returns:
        A MagicMock instance configured to spec UserRepository.
    """
    return MagicMock(spec=UserRepository)


@pytest.fixture
def mock_item_service() -> AsyncMock:
    """Pytest fixture that provides an asynchronous mock ItemService.

    Returns:
        An AsyncMock instance configured to spec ItemService.
    """
    return AsyncMock(spec=ItemService)


@pytest.fixture
def mock_db_session() -> MagicMock:
    """Pytest fixture that provides a mock SQLAlchemy Session.

    Returns:
        A MagicMock instance configured to spec sqlalchemy.orm.Session.
    """
    return MagicMock(spec=Session)
