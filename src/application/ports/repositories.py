from abc import ABC, abstractmethod

from src.application.usecases.analytics.dto import UserCreatedDTO
from src.domain.orders.aggregates import Order
from src.domain.users.entities import User
from src.domain.warehouse.entities import Product


class ABCUserRepository(ABC):
    @abstractmethod
    async def create(self, user: User) -> User:
        raise NotImplementedError


class ABCUserActionAnalyticRepository(ABC):
    @abstractmethod
    async def create(self, dto: UserCreatedDTO) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_total_action_count(self) -> int:
        raise NotImplementedError


class ABCWarehouseRepository(ABC):
    @abstractmethod
    async def get_many(self, ids: list | None = None) -> list[Product]:
        raise NotImplementedError

    @abstractmethod
    async def get_one_by_id(self, id_: int) -> Product:
        raise NotImplementedError


class ABCOrderRepository(ABC):
    @abstractmethod
    async def create(self, order: Order) -> Order:
        raise NotImplementedError


class RepositoryHandler:
    def __init__(
        self,
        user_repository: ABCUserRepository,
        user_analytics_repo: ABCUserActionAnalyticRepository,
        warehouse_repository: ABCWarehouseRepository,
        order_repository: ABCOrderRepository,
    ):
        self.user_repo = user_repository
        self.user_analytics_repo = user_analytics_repo
        self.warehouse_repo = warehouse_repository
        self.order_repo = order_repository
