"""This module provides the SQLAlchemy implementation of the UserRepository interface.

It handles the persistence and retrieval of User and CartItem entities using
SQLAlchemy to interact with a relational database.
"""

from uuid import UUID

from sqlalchemy.orm import Session

from be_task_ca.domain.user.entities import CartItem, User
from be_task_ca.infra.user.models import CartItemModel, UserModel
from be_task_ca.interfaces.user import UserRepository


class SQLAlchemyUserRepository(UserRepository):
    """A repository class for User entities that uses SQLAlchemy for database operations.

    This class implements the UserRepository interface, providing concrete methods
    to save, find, and manage users and their shopping carts in a database
    via SQLAlchemy. It interacts with UserModel and CartItemModel SQLAlchemy models.
    """

    def __init__(self, db: Session) -> None:
        """Initializes the SQLAlchemyUserRepository with a database session.

        Args:
            db: The SQLAlchemy Session to be used for all database operations.
        """
        self.db = db

    def save(self, user: User) -> User:
        """Saves a user to the repository.

        If the user already exists (e.g., based on their ID), they should be updated.
        If it's a new user, they should be created.

        Args:
            user: The User entity to save.

        Returns:
            The saved User entity, potentially with updated fields (e.g., generated ID
            or timestamps).
        """
        db_user = self.db.query(UserModel).filter(UserModel.id == user.id).first()
        if not db_user:
            db_user = UserModel(
                id=user.id,
                email=user.email,
                first_name=user.first_name,
                last_name=user.last_name,
                hashed_password=user.hashed_password,
                shipping_address=user.shipping_address,
            )
            self.db.add(db_user)
        else:
            db_user.email = user.email
            db_user.first_name = user.first_name
            db_user.last_name = user.last_name
            db_user.hashed_password = user.hashed_password
            db_user.shipping_address = user.shipping_address

        # Clear existing cart items and add new ones
        self.db.query(CartItemModel).filter(CartItemModel.user_id == user.id).delete()
        for cart_item in user.cart_items:
            db_cart_item = CartItemModel(
                user_id=cart_item.user_id,
                item_id=cart_item.item_id,
                quantity=cart_item.quantity,
            )
            self.db.add(db_cart_item)

        self.db.commit()
        return user

    def find_by_email(self, email: str) -> User | None:
        """Finds a user by their email address.

        Args:
            email: The email address of the user to find.

        Returns:
            The User entity if found, otherwise None.
        """
        db_user = self.db.query(UserModel).filter(UserModel.email == email).first()
        if db_user:
            cart_items = self.find_cart_items(db_user.id)
            return User(
                id=db_user.id,
                email=db_user.email,
                first_name=db_user.first_name,
                last_name=db_user.last_name,
                hashed_password=db_user.hashed_password,
                shipping_address=db_user.shipping_address,
                cart_items=cart_items,
            )
        return None

    def find_by_id(self, user_id: UUID) -> User | None:
        """Finds a user by their unique identifier.

        Args:
            user_id: The UUID of the user to find.

        Returns:
            The User entity if found, otherwise None.
        """
        db_user = self.db.query(UserModel).filter(UserModel.id == user_id).first()
        if db_user:
            cart_items = self.find_cart_items(db_user.id)
            return User(
                id=db_user.id,
                email=db_user.email,
                first_name=db_user.first_name,
                last_name=db_user.last_name,
                hashed_password=db_user.hashed_password,
                shipping_address=db_user.shipping_address,
                cart_items=cart_items,
            )
        return None

    def find_cart_items(self, user_id: UUID) -> list[CartItem]:
        """Retrieves all cart items associated with a specific user.

        Args:
            user_id: The unique identifier of the user whose cart items are to
                be retrieved.

        Returns:
            A list of CartItem entities. Returns an empty list if the user has
            no cart items or does not exist.
        """
        db_cart_items = (
            self.db.query(CartItemModel).filter(CartItemModel.user_id == user_id).all()
        )
        return [
            CartItem(
                user_id=db_cart_item.user_id,
                item_id=db_cart_item.item_id,
                quantity=db_cart_item.quantity,
            )
            for db_cart_item in db_cart_items
        ]
