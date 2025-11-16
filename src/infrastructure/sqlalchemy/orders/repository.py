from sqlalchemy.ext.asyncio import AsyncSession

from src.application.ports.repositories import ABCOrderRepository
from src.domain.orders.aggregates import Order
from src.infrastructure.sqlalchemy.model import OutboxMessageORM
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
                user_id=order.user_id,
            )
        )
        await self._session.flush()

        order_items = []
        for item in order.items:
            order_item = OrderItemORM(
                order_id=order.id.value,
                product_id=item.product_id.value,
                quantity=item.quantity,
            )
            order_items.append(order_item)
        self._session.add_all(order_items)

        order_events = []
        for event in order.domain_events:
            outbox_event = OutboxMessageORM(
                aggregate_type="order",
                aggregate_id=str(order.id.value),
                event_type=event.event_type,
                payload={
                    **event.dict(),
                },
            )
            order_events.append(outbox_event)
        self._session.add_all(order_events)

        return order
