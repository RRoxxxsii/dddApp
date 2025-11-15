from dataclasses import dataclass
from uuid import UUID

from src.domain.events import DomainEvent


@dataclass
class OrderItemCreatedEvent(DomainEvent):
    title: str
    unit_price: float
    quantity: int


@dataclass
class OrderCreatedEvent(DomainEvent):
    entity_id: UUID
    price: float
    description: str
    items: list[OrderItemCreatedEvent]
    user_id: int
    email: str
