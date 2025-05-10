from uuid import uuid4
import pytest
from be_task_ca.domain.item.usecases import CreateItemUseCase, GetAllItemsUseCase
from be_task_ca.domain.item.entities import Item
from be_task_ca.domain.item.schema import (
    CreateItemRequest,
    CreateItemResponse,
    AllItemsResponse,
)
from decimal import Decimal


class TestCreateItemUseCase:
    @pytest.fixture(autouse=True)
    def setup(self, mock_item_repository):
        self.item_repository = mock_item_repository
        self.use_case = CreateItemUseCase(self.item_repository)

    @pytest.fixture
    def create_item_request(self):
        return CreateItemRequest(
            name="Test Item", description=None, price=Decimal("10.0"), quantity=5
        )

    def test_execute_success(self, create_item_request):
        # Arrange
        item = Item(
            id=uuid4(),
            name="Test Item",
            description=None,
            price=Decimal("10.0"),
            quantity=5,
        )
        self.item_repository.find_by_name.return_value = None
        self.item_repository.save.return_value = item

        # Act
        result = self.use_case.execute(create_item_request)

        # Assert
        assert isinstance(result, CreateItemResponse)
        assert result.name == "Test Item"
        assert result.price == Decimal("10.0")
        assert result.quantity == 5
        self.item_repository.find_by_name.assert_called_once_with("Test Item")
        self.item_repository.save.assert_called_once()

    def test_execute_conflict(self, create_item_request):
        # Arrange
        existing_item = Item(
            id=uuid4(),
            name="Test Item",
            description=None,
            price=Decimal("10.0"),
            quantity=5,
        )
        self.item_repository.find_by_name.return_value = existing_item

        # Act/Assert
        with pytest.raises(ValueError) as exc:
            self.use_case.execute(create_item_request)
        assert str(exc.value) == "An item with this name already exists"
        self.item_repository.find_by_name.assert_called_once_with("Test Item")
        self.item_repository.save.assert_not_called()


class TestGetAllItemsUseCase:
    @pytest.fixture(autouse=True)
    def setup(self, mock_item_repository):
        self.item_repository = mock_item_repository
        self.use_case = GetAllItemsUseCase(self.item_repository)

    def test_execute_success(self):
        # Arrange
        item1 = Item(
            id=uuid4(),
            name="Item 1",
            description=None,
            price=Decimal("10.0"),
            quantity=5,
        )
        item2 = Item(
            id=uuid4(),
            name="Item 2",
            description="Desc",
            price=Decimal("20.0"),
            quantity=3,
        )
        self.item_repository.get_all.return_value = [item1, item2]

        # Act
        result = self.use_case.execute()

        # Assert
        assert isinstance(result, AllItemsResponse)
        assert len(result.items) == 2
        assert result.items[0].name == "Item 1"
        assert result.items[1].name == "Item 2"
        self.item_repository.get_all.assert_called_once()

    def test_execute_empty(self):
        # Arrange
        self.item_repository.get_all.return_value = []

        # Act
        result = self.use_case.execute()

        # Assert
        assert isinstance(result, AllItemsResponse)
        assert len(result.items) == 0
        self.item_repository.get_all.assert_called_once()
