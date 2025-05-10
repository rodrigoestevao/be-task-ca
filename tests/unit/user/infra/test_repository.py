from unittest.mock import MagicMock
from uuid import uuid4
import pytest
from be_task_ca.infra.user.sqlalchemy_repository import SQLAlchemyUserRepository
from be_task_ca.infra.user.in_memory_repository import InMemoryUserRepository
from be_task_ca.domain.user.entities import User, CartItem
from be_task_ca.infra.user.models import UserModel, CartItemModel


class TestSQLAlchemyUserRepository:
    @pytest.fixture(autouse=True)
    def setup(self, mock_db_session):
        self.db = mock_db_session
        self.repository = SQLAlchemyUserRepository(self.db)

    def test_save_new_user(self):
        user = User(
            id=uuid4(),
            email="john.doe@example.com",
            first_name="John",
            last_name="Doe",
            hashed_password="hashed_password",
            shipping_address=None,
            cart_items=[],
        )
        self.db.query.return_value.filter.return_value.first.return_value = None
        self.db.add = MagicMock()
        self.db.commit = MagicMock()
        result = self.repository.save(user)
        assert result == user
        self.db.add.assert_called_once()
        self.db.commit.assert_called_once()
        assert isinstance(self.db.add.call_args[0][0], UserModel)

    def test_save_existing_user(self):
        user_id = uuid4()
        user = User(
            id=user_id,
            email="john.doe@example.com",
            first_name="John",
            last_name="Doe",
            hashed_password="hashed_password",
            shipping_address=None,
            cart_items=[],
        )
        db_user = UserModel(
            id=user_id,
            email="old@example.com",
            first_name="Old",
            last_name="Name",
            hashed_password="old_password",
            shipping_address="Old Address",
        )
        self.db.query.return_value.filter.return_value.first.return_value = db_user
        self.db.commit = MagicMock()
        result = self.repository.save(user)
        assert result == user
        assert db_user.email == user.email
        assert db_user.first_name == user.first_name
        self.db.commit.assert_called_once()

    def test_save_with_cart_items(self):
        user_id = uuid4()
        cart_item = CartItem(user_id=user_id, item_id=uuid4(), quantity=2)
        user = User(
            id=user_id,
            email="john.doe@example.com",
            first_name="John",
            last_name="Doe",
            hashed_password="hashed_password",
            shipping_address=None,
            cart_items=[cart_item],
        )
        self.db.query.return_value.filter.return_value.first.return_value = None
        self.db.add = MagicMock()
        self.db.commit = MagicMock()
        self.db.query.return_value.filter.return_value.delete = MagicMock()
        result = self.repository.save(user)
        assert result == user
        assert self.db.add.call_count == 2  # User and CartItem
        self.db.commit.assert_called_once()
        self.db.query.return_value.filter.return_value.delete.assert_called_once()

    def test_find_by_email_found(self):
        user_id = uuid4()
        db_user = UserModel(
            id=user_id,
            email="john.doe@example.com",
            first_name="John",
            last_name="Doe",
            hashed_password="hashed_password",
            shipping_address=None,
        )
        self.db.query.return_value.filter.return_value.first.return_value = db_user
        self.db.query.return_value.filter.return_value.all.return_value = []
        result = self.repository.find_by_email("john.doe@example.com")
        assert isinstance(result, User)
        assert result.email == "john.doe@example.com"
        assert result.cart_items == []
        self.db.query.assert_any_call(UserModel)

    def test_find_by_email_not_found(self):
        self.db.query.return_value.filter.return_value.first.return_value = None
        result = self.repository.find_by_email("john.doe@example.com")
        assert result is None
        self.db.query.assert_called_with(UserModel)

    def test_find_by_id_found(self):
        user_id = uuid4()
        db_user = UserModel(
            id=user_id,
            email="john.doe@example.com",
            first_name="John",
            last_name="Doe",
            hashed_password="hashed_password",
            shipping_address=None,
        )
        self.db.query.return_value.filter.return_value.first.return_value = db_user
        self.db.query.return_value.filter.return_value.all.return_value = []
        result = self.repository.find_by_id(user_id)
        assert isinstance(result, User)
        assert result.id == user_id
        self.db.query.assert_any_call(UserModel)

    def test_find_by_id_not_found(self):
        user_id = uuid4()
        self.db.query.return_value.filter.return_value.first.return_value = None
        result = self.repository.find_by_id(user_id)
        assert result is None
        self.db.query.assert_called_with(UserModel)

    def test_find_cart_items(self):
        user_id = uuid4()
        db_cart_item = CartItemModel(user_id=user_id, item_id=uuid4(), quantity=2)
        self.db.query.return_value.filter.return_value.all.return_value = [db_cart_item]
        result = self.repository.find_cart_items(user_id)
        assert len(result) == 1
        assert isinstance(result[0], CartItem)
        assert result[0].quantity == 2
        self.db.query.assert_called_with(CartItemModel)


class TestInMemoryUserRepository:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.repository = InMemoryUserRepository()

    def test_save_new_user(self):
        user = User(
            id=uuid4(),
            email="john.doe@example.com",
            first_name="John",
            last_name="Doe",
            hashed_password="hashed_password",
            shipping_address=None,
            cart_items=[],
        )
        result = self.repository.save(user)
        assert result == user
        assert self.repository.find_by_id(user.id) == user

    def test_save_existing_user(self):
        user_id = uuid4()
        user = User(
            id=user_id,
            email="john.doe@example.com",
            first_name="John",
            last_name="Doe",
            hashed_password="hashed_password",
            shipping_address=None,
            cart_items=[],
        )
        self.repository.save(user)
        updated_user = User(
            id=user_id,
            email="jane.doe@example.com",
            first_name="Jane",
            last_name="Doe",
            hashed_password="new_password",
            shipping_address="123 Main St",
            cart_items=[],
        )
        result = self.repository.save(updated_user)
        assert result == updated_user
        assert self.repository.find_by_id(user_id).email == "jane.doe@example.com"

    def test_save_with_cart_items(self):
        user_id = uuid4()
        cart_item = CartItem(user_id=user_id, item_id=uuid4(), quantity=2)
        user = User(
            id=user_id,
            email="john.doe@example.com",
            first_name="John",
            last_name="Doe",
            hashed_password="hashed_password",
            shipping_address=None,
            cart_items=[cart_item],
        )
        result = self.repository.save(user)
        assert result == user
        assert len(self.repository.find_cart_items(user_id)) == 1
        assert self.repository.find_cart_items(user_id)[0].quantity == 2

    def test_find_by_email_found(self):
        user = User(
            id=uuid4(),
            email="john.doe@example.com",
            first_name="John",
            last_name="Doe",
            hashed_password="hashed_password",
            shipping_address=None,
            cart_items=[],
        )
        self.repository.save(user)
        result = self.repository.find_by_email("john.doe@example.com")
        assert isinstance(result, User)
        assert result.email == "john.doe@example.com"

    def test_find_by_email_not_found(self):
        result = self.repository.find_by_email("john.doe@example.com")
        assert result is None

    def test_find_by_id_found(self):
        user_id = uuid4()
        user = User(
            id=user_id,
            email="john.doe@example.com",
            first_name="John",
            last_name="Doe",
            hashed_password="hashed_password",
            shipping_address=None,
            cart_items=[],
        )
        self.repository.save(user)
        result = self.repository.find_by_id(user_id)
        assert isinstance(result, User)
        assert result.id == user_id

    def test_find_by_id_not_found(self):
        user_id = uuid4()
        result = self.repository.find_by_id(user_id)
        assert result is None

    def test_find_cart_items(self):
        user_id = uuid4()
        cart_item = CartItem(user_id=user_id, item_id=uuid4(), quantity=2)
        user = User(
            id=user_id,
            email="john.doe@example.com",
            first_name="John",
            last_name="Doe",
            hashed_password="hashed_password",
            shipping_address=None,
            cart_items=[cart_item],
        )
        self.repository.save(user)
        result = self.repository.find_cart_items(user_id)
        assert len(result) == 1
        assert isinstance(result[0], CartItem)
        assert result[0].quantity == 2

    def test_find_cart_items_user_not_found(self):
        user_id = uuid4()
        result = self.repository.find_cart_items(user_id)
        assert result == []
