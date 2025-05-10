from unittest.mock import MagicMock
from uuid import uuid4
import pytest
from be_task_ca.infra.item.sqlalchemy_repository import SQLAlchemyItemRepository
from be_task_ca.infra.item.in_memory_repository import InMemoryItemRepository
from be_task_ca.domain.item.entities import Item
from be_task_ca.infra.item.models import ItemModel
from decimal import Decimal


class TestSQLAlchemyItemRepository:
    @pytest.fixture(autouse=True)
    def setup(self, mock_db_session):
        self.db = mock_db_session
        self.repository = SQLAlchemyItemRepository(self.db)

    def test_save_new_item(self):
        item = Item(
            id=uuid4(),
            name="Test Item",
            description="A test item",
            quantity=10,
            price=Decimal("19.99"),
        )
        self.db.query.return_value.filter.return_value.first.return_value = None
        self.db.add = MagicMock()
        self.db.commit = MagicMock()
        result = self.repository.save(item)
        assert result == item
        self.db.add.assert_called_once()
        self.db.commit.assert_called_once()
        assert isinstance(self.db.add.call_args[0][0], ItemModel)
        assert self.db.add.call_args[0][0].price == Decimal("19.99")

    def test_save_existing_item(self):
        item_id = uuid4()
        item = Item(
            id=item_id,
            name="Test Item",
            description="A test item",
            quantity=10,
            price=Decimal("19.99"),
        )
        db_item = ItemModel(
            id=item_id,
            name="Old Item",
            description="Old description",
            quantity=5,
            price=Decimal("9.99"),
        )
        self.db.query.return_value.filter.return_value.first.return_value = db_item
        self.db.commit = MagicMock()
        result = self.repository.save(item)
        assert result == item
        assert db_item.name == item.name
        assert db_item.quantity == item.quantity
        assert db_item.price == item.price
        self.db.commit.assert_called_once()

    def test_find_by_id_found(self):
        item_id = uuid4()
        db_item = ItemModel(
            id=item_id,
            name="Test Item",
            description="A test item",
            quantity=10,
            price=Decimal("19.99"),
        )
        self.db.query.return_value.filter.return_value.first.return_value = db_item
        result = self.repository.find_by_id(item_id)
        assert isinstance(result, Item)
        assert result.id == item_id
        assert result.name == "Test Item"
        assert result.price == Decimal("19.99")
        self.db.query.assert_called_with(ItemModel)

    def test_find_by_id_not_found(self):
        item_id = uuid4()
        self.db.query.return_value.filter.return_value.first.return_value = None
        result = self.repository.find_by_id(item_id)
        assert result is None
        self.db.query.assert_called_with(ItemModel)

    def test_find_by_name_found(self):
        db_item = ItemModel(
            id=uuid4(),
            name="Test Item",
            description="A test item",
            quantity=10,
            price=Decimal("19.99"),
        )
        self.db.query.return_value.filter.return_value.first.return_value = db_item
        result = self.repository.find_by_name("Test Item")
        assert isinstance(result, Item)
        assert result.name == "Test Item"
        assert result.price == Decimal("19.99")
        self.db.query.assert_called_with(ItemModel)

    def test_find_by_name_not_found(self):
        self.db.query.return_value.filter.return_value.first.return_value = None
        result = self.repository.find_by_name("Nonexistent Item")
        assert result is None
        self.db.query.assert_called_with(ItemModel)

    def test_get_all(self):
        db_item = ItemModel(
            id=uuid4(),
            name="Test Item",
            description="A test item",
            quantity=10,
            price=Decimal("19.99"),
        )
        self.db.query.return_value.all.return_value = [db_item]
        result = self.repository.get_all()
        assert len(result) == 1
        assert isinstance(result[0], Item)
        assert result[0].name == "Test Item"
        assert result[0].price == Decimal("19.99")
        self.db.query.assert_called_with(ItemModel)


class TestInMemoryItemRepository:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.repository = InMemoryItemRepository()

    def test_save_new_item(self):
        item = Item(
            id=uuid4(),
            name="Test Item",
            description="A test item",
            quantity=10,
            price=Decimal("19.99"),
        )
        result = self.repository.save(item)
        assert result == item
        existing = self.repository.find_by_id(item.id)
        assert existing is not None
        assert existing == item
        assert existing.price == Decimal("19.99")

    def test_save_existing_item(self):
        item_id = uuid4()
        item = Item(
            id=item_id,
            name="Test Item",
            description="A test item",
            quantity=10,
            price=Decimal("19.99"),
        )
        self.repository.save(item)
        updated_item = Item(
            id=item_id,
            name="Updated Item",
            description="Updated description",
            quantity=20,
            price=Decimal("29.99"),
        )
        result = self.repository.save(updated_item)
        assert result == updated_item
        existing = self.repository.find_by_id(item_id)
        assert existing is not None
        assert existing.name == "Updated Item"
        assert existing.quantity == 20
        assert existing.price == Decimal("29.99")

    def test_find_by_id_found(self):
        item_id = uuid4()
        item = Item(
            id=item_id,
            name="Test Item",
            description="A test item",
            quantity=10,
            price=Decimal("19.99"),
        )
        self.repository.save(item)
        result = self.repository.find_by_id(item_id)
        assert isinstance(result, Item)
        assert result.id == item_id
        assert result.name == "Test Item"
        assert result.price == Decimal("19.99")

    def test_find_by_id_not_found(self):
        item_id = uuid4()
        result = self.repository.find_by_id(item_id)
        assert result is None

    def test_find_by_name_found(self):
        item = Item(
            id=uuid4(),
            name="Test Item",
            description="A test item",
            quantity=10,
            price=Decimal("19.99"),
        )
        self.repository.save(item)
        result = self.repository.find_by_name("Test Item")
        assert isinstance(result, Item)
        assert result.name == "Test Item"
        assert result.price == Decimal("19.99")

    def test_find_by_name_not_found(self):
        result = self.repository.find_by_name("Nonexistent Item")
        assert result is None

    def test_get_all(self):
        item1 = Item(
            id=uuid4(),
            name="Test Item 1",
            description="First test item",
            quantity=10,
            price=Decimal("19.99"),
        )
        item2 = Item(
            id=uuid4(),
            name="Test Item 2",
            description="Second test item",
            quantity=20,
            price=Decimal("29.99"),
        )
        self.repository.save(item1)
        self.repository.save(item2)
        result = self.repository.get_all()
        assert len(result) == 2
        assert item1 in result
        assert item2 in result
        assert result[0].price in [Decimal("19.99"), Decimal("29.99")]
        assert result[1].price in [Decimal("19.99"), Decimal("29.99")]
