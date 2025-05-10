from uuid import UUID, uuid4
import pytest
from be_task_ca.user.entities import User, CartItem


class TestUserEntity:
    @pytest.fixture
    def user_data(self):
        return {
            "id": uuid4(),
            "email": "john.doe@example.com",
            "first_name": "John",
            "last_name": "Doe",
            "hashed_password": "hashed_password",
            "shipping_address": None,
            "cart_items": [],
        }

    def test_user_initialization(self, user_data):
        # Arrange/Act
        user = User(**user_data)

        # Assert
        assert user.id == user_data["id"]
        assert user.email == user_data["email"]
        assert user.first_name == user_data["first_name"]
        assert user.last_name == user_data["last_name"]
        assert user.hashed_password == user_data["hashed_password"]
        assert user.shipping_address == user_data["shipping_address"]
        assert user.cart_items == user_data["cart_items"]

    def test_user_with_cart_items(self, user_data):
        # Arrange
        cart_item = CartItem(user_id=user_data["id"], item_id=uuid4(), quantity=2)
        user_data["cart_items"] = [cart_item]

        # Act
        user = User(**user_data)

        # Assert
        assert len(user.cart_items) == 1
        assert user.cart_items[0].quantity == 2

    def test_user_null_shipping_address(self, user_data):
        # Arrange
        user_data["shipping_address"] = None

        # Act
        user = User(**user_data)

        # Assert
        assert user.shipping_address is None


class TestCartItemEntity:
    @pytest.fixture
    def cart_item_data(self):
        return {"user_id": uuid4(), "item_id": uuid4(), "quantity": 2}

    def test_cart_item_initialization(self, cart_item_data):
        # Arrange/Act
        cart_item = CartItem(**cart_item_data)

        # Assert
        assert cart_item.user_id == cart_item_data["user_id"]
        assert cart_item.item_id == cart_item_data["item_id"]
        assert cart_item.quantity == cart_item_data["quantity"]

    def test_cart_item_invalid_quantity(self, cart_item_data):
        # Arrange
        cart_item_data["quantity"] = 0

        # Act/Assert
        with pytest.raises(ValueError):
            CartItem(**cart_item_data)
