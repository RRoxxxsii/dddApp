from dataclasses import dataclass
from decimal import Decimal

from src.domain.analytics.entity import ActionTypeEnum
from src.domain.entities import BaseEntity
from src.domain.orders.entities import OrderItem
from src.domain.orders.events import OrderCreatedEvent, OrderItemCreatedEvent
from src.domain.orders.valueobjects import OrderId
from src.domain.warehouse.valueobjects import Money


@dataclass
class Order(BaseEntity):
    id: OrderId
    price: Money
    description: str
    items: list[OrderItem]
    user_id: int

    @classmethod
    def create(
        cls,
        id_: OrderId,
        description: str,
        items: list[OrderItem],
        user_id: int,
        email: str,
    ) -> "Order":
        price = Money(amount=Decimal(0))
        for item in items:
            price += item.unit_price

        event = OrderCreatedEvent(
            entity_id=id_.value,
            event_type=ActionTypeEnum.ORDER_CREATED.value,
            description=description,
            items=[
                OrderItemCreatedEvent(
                    entity_id=None,
                    event_type=ActionTypeEnum.ORDER_CREATED.value,
                    unit_price=float(item.unit_price.amount),
                    quantity=item.quantity,
                    title=item.title,
                )
                for item in items
            ],
            price=float(price.amount),
            user_id=user_id,
            email=email,
        )

        order = Order(
            id=id_,
            price=price,
            description=description,
            items=items,
            user_id=user_id,
            _domain_events=list(),
        )
        order._add_domain_event(event)

        return order
