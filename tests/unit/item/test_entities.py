from uuid import UUID, uuid4
import pytest
from be_task_ca.domain.item.entities import Item
from decimal import Decimal


class TestItemEntity:
    @pytest.fixture
    def item_data(self):
        return {
            "id": uuid4(),
            "name": "Test Item",
            "description": "A test item",
            "price": Decimal("10.0"),
            "quantity": 5,
        }

    def test_item_initialization(self, item_data):
        # Arrange/Act
        item = Item(**item_data)

        # Assert
        assert item.id == item_data["id"]
        assert item.name == item_data["name"]
        assert item.description == item_data["description"]
        assert item.price == item_data["price"]
        assert item.quantity == item_data["quantity"]

    def test_item_null_description(self, item_data):
        # Arrange
        item_data["description"] = None

        # Act
        item = Item(**item_data)

        # Assert
        assert item.description is None

    def test_item_negative_price(self, item_data):
        # Arrange
        item_data["price"] = Decimal("-1.0")

        # Act/Assert
        with pytest.raises(ValueError) as exc:
            Item(**item_data)
        assert str(exc.value) == "Price cannot be negative"

    def test_item_negative_quantity(self, item_data):
        # Arrange
        item_data["quantity"] = -1

        # Act/Assert
        with pytest.raises(ValueError) as exc:
            Item(**item_data)
        assert str(exc.value) == "Quantity cannot be negative"

    def test_item_zero_price(self, item_data):
        # Arrange
        item_data["price"] = Decimal("0.0")

        # Act
        item = Item(**item_data)

        # Assert
        assert item.price == Decimal("0.0")

    def test_item_zero_quantity(self, item_data):
        # Arrange
        item_data["quantity"] = 0

        # Act
        item = Item(**item_data)

        # Assert
        assert item.quantity == 0
