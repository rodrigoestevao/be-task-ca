from uuid import uuid4
import pytest
import asyncio
from be_task_ca.domain.user.usecases import (
    CreateUserUseCase,
    AddItemToCartUseCase,
    ListItemsInCartUseCase,
)
from be_task_ca.domain.user.entities import User, CartItem
from be_task_ca.domain.user.schema import (
    CreateUserRequest,
    CreateUserResponse,
    AddToCartRequest,
    AddToCartResponse,
)


class TestCreateUserUseCase:
    @pytest.fixture(autouse=True)
    def setup(self, mock_user_repository):
        self.user_repository = mock_user_repository
        self.use_case = CreateUserUseCase(self.user_repository)

    @pytest.fixture
    def create_user_request(self):
        return CreateUserRequest(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            password="password",
            shipping_address=None,
        )

    def test_execute_success(self, create_user_request):
        # Arrange
        user = User(
            id=uuid4(),
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            hashed_password="hashed_password",
            shipping_address=None,
            cart_items=[],
        )
        self.user_repository.find_by_email.return_value = None
        self.user_repository.save.return_value = user

        # Act
        result = self.use_case.execute(create_user_request)

        # Assert
        assert isinstance(result, CreateUserResponse)
        assert result.email == "john.doe@example.com"
        assert result.first_name == "John"
        self.user_repository.find_by_email.assert_called_once_with(
            "john.doe@example.com"
        )
        self.user_repository.save.assert_called_once()

    def test_execute_conflict(self, create_user_request):
        # Arrange
        existing_user = User(
            id=uuid4(),
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            hashed_password="hashed_password",
            shipping_address=None,
            cart_items=[],
        )
        self.user_repository.find_by_email.return_value = existing_user

        # Act/Assert
        with pytest.raises(ValueError) as exc:
            self.use_case.execute(create_user_request)
        assert str(exc.value) == "An user with this email already exists"
        self.user_repository.find_by_email.assert_called_once_with(
            "john.doe@example.com"
        )
        self.user_repository.save.assert_not_called()


class TestAddItemToCartUseCase:
    @pytest.fixture(autouse=True)
    def setup(self, mock_user_repository, mock_item_service):
        self.user_repository = mock_user_repository
        self.item_service = mock_item_service
        self.use_case = AddItemToCartUseCase(self.user_repository, self.item_service)

    @pytest.fixture
    def add_to_cart_request(self):
        return AddToCartRequest(item_id=uuid4(), quantity=2)

    @pytest.mark.asyncio
    async def test_execute_success(self, add_to_cart_request):
        # Arrange
        user_id = uuid4()
        user = User(
            id=user_id,
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            hashed_password="hashed_password",
            shipping_address=None,
            cart_items=[],
        )
        item = {"id": add_to_cart_request.item_id, "name": "Test Item", "quantity": 5}
        self.user_repository.find_by_id.return_value = user
        self.item_service.get_item.return_value = item
        self.item_service.check_stock.return_value = True
        self.user_repository.save.return_value = user

        # Act
        result = await self.use_case.execute(user_id, add_to_cart_request)

        # Assert
        assert isinstance(result, AddToCartResponse)
        assert len(result.items) == 1
        assert result.items[0].item_id == add_to_cart_request.item_id
        assert result.items[0].quantity == 2
        self.user_repository.find_by_id.assert_called_once_with(user_id)
        self.item_service.get_item.assert_called_once_with(add_to_cart_request.item_id)
        self.item_service.check_stock.assert_called_once_with(
            add_to_cart_request.item_id, quantity=2
        )
        self.user_repository.save.assert_called_once()

    @pytest.mark.asyncio
    async def test_execute_user_not_found(self, add_to_cart_request):
        # Arrange
        user_id = uuid4()
        self.user_repository.find_by_id.return_value = None

        # Act/Assert
        with pytest.raises(ValueError) as exc:
            await self.use_case.execute(user_id, add_to_cart_request)
        assert str(exc.value) == "User does not exists"
        self.user_repository.find_by_id.assert_called_once_with(user_id)
        self.item_service.get_item.assert_not_called()
        self.item_service.check_stock.assert_not_called()
        self.user_repository.save.assert_not_called()

    @pytest.mark.asyncio
    async def test_execute_item_not_found(self, add_to_cart_request):
        # Arrange
        user_id = uuid4()
        user = User(
            id=user_id,
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            hashed_password="hashed_password",
            shipping_address=None,
            cart_items=[],
        )
        self.user_repository.find_by_id.return_value = user
        self.item_service.get_item.return_value = None

        # Act/Assert
        with pytest.raises(ValueError) as exc:
            await self.use_case.execute(user_id, add_to_cart_request)
        assert str(exc.value) == "Item does not exists"
        self.user_repository.find_by_id.assert_called_once_with(user_id)
        self.item_service.get_item.assert_called_once_with(add_to_cart_request.item_id)
        self.item_service.check_stock.assert_not_called()
        self.user_repository.save.assert_not_called()

    @pytest.mark.asyncio
    async def test_execute_insufficient_stock(self, add_to_cart_request):
        # Arrange
        user_id = uuid4()
        user = User(
            id=user_id,
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            hashed_password="hashed_password",
            shipping_address=None,
            cart_items=[],
        )
        item = {"id": add_to_cart_request.item_id, "name": "Test Item", "quantity": 1}
        self.user_repository.find_by_id.return_value = user
        self.item_service.get_item.return_value = item
        self.item_service.check_stock.return_value = False

        # Act/Assert
        with pytest.raises(ValueError) as exc:
            await self.use_case.execute(user_id, add_to_cart_request)
        assert str(exc.value) == "Not enough items in stock"
        self.user_repository.find_by_id.assert_called_once_with(user_id)
        self.item_service.get_item.assert_called_once_with(add_to_cart_request.item_id)
        self.item_service.check_stock.assert_called_once_with(
            add_to_cart_request.item_id, quantity=2
        )
        self.user_repository.save.assert_not_called()

    @pytest.mark.asyncio
    async def test_execute_item_already_in_cart(self, add_to_cart_request):
        # Arrange
        user_id = uuid4()
        cart_item = CartItem(
            user_id=user_id, item_id=add_to_cart_request.item_id, quantity=1
        )
        user = User(
            id=user_id,
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            hashed_password="hashed_password",
            shipping_address=None,
            cart_items=[cart_item],
        )
        item = {"id": add_to_cart_request.item_id, "name": "Test Item", "quantity": 5}
        self.user_repository.find_by_id.return_value = user
        self.item_service.get_item.return_value = item
        self.item_service.check_stock.return_value = True

        # Act/Assert
        with pytest.raises(ValueError) as exc:
            await self.use_case.execute(user_id, add_to_cart_request)
        assert str(exc.value) == "Item already in cart"
        self.user_repository.find_by_id.assert_called_once_with(user_id)
        self.item_service.get_item.assert_called_once_with(add_to_cart_request.item_id)
        self.item_service.check_stock.assert_called_once_with(
            add_to_cart_request.item_id, quantity=2
        )
        self.user_repository.save.assert_not_called()


class TestListItemsInCartUseCase:
    @pytest.fixture(autouse=True)
    def setup(self, mock_user_repository):
        self.user_repository = mock_user_repository
        self.use_case = ListItemsInCartUseCase(self.user_repository)

    def test_execute_success(self):
        # Arrange
        user_id = uuid4()
        cart_item = CartItem(user_id=user_id, item_id=uuid4(), quantity=2)
        self.user_repository.find_cart_items.return_value = [cart_item]

        # Act
        result = self.use_case.execute(user_id)

        # Assert
        assert isinstance(result, AddToCartResponse)
        assert len(result.items) == 1
        assert result.items[0].quantity == 2
        assert result.items[0].item_id == cart_item.item_id
        self.user_repository.find_cart_items.assert_called_once_with(user_id)

    def test_execute_empty_cart(self):
        # Arrange
        user_id = uuid4()
        self.user_repository.find_cart_items.return_value = []

        # Act
        result = self.use_case.execute(user_id)

        # Assert
        assert isinstance(result, AddToCartResponse)
        assert len(result.items) == 0
        self.user_repository.find_cart_items.assert_called_once_with(user_id)
