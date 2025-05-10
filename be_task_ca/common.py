from collections.abc import Iterator

from fastapi import Request

from be_task_ca.database import SessionLocal


def get_db(request: Request) -> Iterator:  # noqa: ARG001
    """Dependency that provides a database session.

    It creates a new database session for each request and ensures
    that the session is closed after the request is completed.

    Args:
        request: The incoming FastAPI request. Not used directly in the function
        but required by FastAPI's dependency injection.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
