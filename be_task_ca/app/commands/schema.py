"""This module provides command-line interface (CLI) commands for the application.

Currently, it includes a command to create the database schema based on
SQLAlchemy models. Importing the models here ensures they are registered
with SQLAlchemy's metadata before the schema creation is attempted.
"""

from be_task_ca.infra.database import Base, engine

# just importing all the models is enough to have them created
from be_task_ca.infra.item.models import ItemModel  # noqa: F401
from be_task_ca.infra.user.models import CartItemModel, UserModel  # noqa: F401


def create_db_schema() -> None:
    """Creates all database tables defined by SQLAlchemy models.

    This function uses the metadata associated with the `Base` declarative
    base class to issue CREATE TABLE statements to the database connected
    via `engine`.
    """
    Base.metadata.create_all(bind=engine)
