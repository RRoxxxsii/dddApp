from sqlalchemy.ext.asyncio import AsyncSession

from src.application.ports.repositories import ABCOrderRepository
from src.domain.orders.aggregates import Order
from src.infrastructure.sqlalchemy.orders.model import OrderItemORM, OrderORM


class OrderRepository(ABCOrderRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, order: Order) -> Order:
        self._session.add(
            OrderORM(
                id=order.id.value,
                price=order.price.amount,
                description=order.description,
            )
        )

        order_items = []
        for item in order.items:
            order_item = OrderItemORM(
                order_id=order.id.value,
                product_id=item.product_id,
                quantity=item.quantity,
            )
            order_items.append(order_item)

        await self._session.flush()
        return order
