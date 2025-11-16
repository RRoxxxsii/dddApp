from src.application.ports.event_bus import ABCEventBus
from src.application.ports.repositories import RepositoryHandler
from src.application.usecases.orders.dto import OrderDTO
from src.application.usecases.orders.mapper import OrderMapper
from src.domain.exceptions import NotFoundException
from src.domain.orders.aggregates import Order
from src.domain.orders.entities import OrderItem
from src.domain.orders.valueobjects import OrderId
from src.domain.usecase import BaseUseCase
from src.infrastructure.sqlalchemy.uow import UnitOfWork
from src.presentation.api.orders.schema import CreateOrder


class CreateOrderUseCase(BaseUseCase):
    def __init__(
        self,
        uow: UnitOfWork,
        repository_handler: RepositoryHandler,
        event_bus: ABCEventBus,
    ) -> None:
        super().__init__(uow=uow, repository_handler=repository_handler)
        self._repository_handler = repository_handler
        self._mapper = OrderMapper
        self._event_bus = event_bus

    async def __call__(self, dto: CreateOrder) -> OrderDTO:
        products = await self._repository_handler.warehouse_repo.get_many(
            ids=[product.product_id for product in dto.products]
        )
        if len(products) == 0:
            raise NotFoundException(message="Products with ids do not exist.")

        product_to_quantity = {
            product.product_id: product.quantity for product in dto.products
        }
        order_items = []
        for product in products:
            order_item = OrderItem.create(
                product_id=product.id,
                quantity=product_to_quantity[product.id.value],
                unit_price=product.price,
                title=product.title,
            )
            order_items.append(order_item)

        order = Order.create(
            id_=OrderId(),
            description="",
            items=order_items,
            user_id=dto.user_id,
            email=dto.email,
        )

        await self._repository_handler.order_repo.create(order)
        await self._uow.commit()

        order.clear_domain_events()
        return self._mapper.map_order(order)


class OrderInteractor:
    def __init__(
        self,
        uow: UnitOfWork,
        repository_handler: RepositoryHandler,
        event_bus: ABCEventBus,
    ) -> None:
        self._uow = uow
        self._repository_handler = repository_handler
        self._event_bus = event_bus

    async def create_order(self, dto: CreateOrder) -> OrderDTO:
        return await CreateOrderUseCase(
            self._uow, self._repository_handler, self._event_bus
        )(dto)
