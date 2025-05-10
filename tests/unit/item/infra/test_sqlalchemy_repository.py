from unittest.mock import MagicMock
from uuid import uuid4
import pytest
from be_task_ca.infra.item.sqlalchemy_repository import SQLAlchemyItemRepository
from be_task_ca.domain.item.entities import Item
from be_task_ca.infra.item.models import ItemModel
from decimal import Decimal


class TestSQLAlchemyItemRepository:
    @pytest.fixture(autouse=True)
    def setup(self, mock_db_session):
        self.db = mock_db_session
        self.repository = SQLAlchemyItemRepository(self.db)

    def test_save(self):
        # Arrange
        item = Item(
            id=uuid4(),
            name="Test Item",
            description=None,
            price=Decimal("10.0"),
            quantity=5,
        )
        self.db.add = MagicMock()
        self.db.commit = MagicMock()

        # Act
        result = self.repository.save(item)

        # Assert
        assert result == item
        self.db.add.assert_called_once()
        self.db.commit.assert_called_once()
        assert isinstance(self.db.add.call_args[0][0], ItemModel)

    def test_find_by_name_found(self):
        # Arrange
        db_item = ItemModel(
            id=uuid4(),
            name="Test Item",
            description=None,
            price=Decimal("10.0"),
            quantity=5,
        )
        self.db.query.return_value.filter.return_value.first.return_value = db_item

        # Act
        result = self.repository.find_by_name("Test Item")

        # Assert
        assert isinstance(result, Item)
        assert result.name == "Test Item"
        self.db.query.assert_called_once_with(ItemModel)

    def test_find_by_name_not_found(self):
        # Arrange
        self.db.query.return_value.filter.return_value.first.return_value = None

        # Act
        result = self.repository.find_by_name("Test Item")

        # Assert
        assert result is None
        self.db.query.assert_called_once_with(ItemModel)

    def test_find_by_id_found(self):
        # Arrange
        item_id = uuid4()
        db_item = ItemModel(
            id=item_id,
            name="Test Item",
            description=None,
            price=Decimal("10.0"),
            quantity=5,
        )
        self.db.query.return_value.filter.return_value.first.return_value = db_item

        # Act
        result = self.repository.find_by_id(item_id)

        # Assert
        assert isinstance(result, Item)
        assert result.id == item_id
        self.db.query.assert_called_once_with(ItemModel)

    def test_find_by_id_not_found(self):
        # Arrange
        item_id = uuid4()
        self.db.query.return_value.filter.return_value.first.return_value = None

        # Act
        result = self.repository.find_by_id(item_id)

        # Assert
        assert result is None
        self.db.query.assert_called_once_with(ItemModel)

    def test_get_all(self):
        # Arrange
        db_item1 = ItemModel(
            id=uuid4(),
            name="Item 1",
            description=None,
            price=Decimal("10.0"),
            quantity=5,
        )
        db_item2 = ItemModel(
            id=uuid4(), name="Item 2", description="Desc", price=20.0, quantity=3
        )
        self.db.query.return_value.all.return_value = [db_item1, db_item2]

        # Act
        result = self.repository.get_all()

        # Assert
        assert len(result) == 2
        assert all(isinstance(item, Item) for item in result)
        assert result[0].name == "Item 1"
        assert result[1].name == "Item 2"
        self.db.query.assert_called_once_with(ItemModel)
