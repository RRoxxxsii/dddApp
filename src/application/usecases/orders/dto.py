from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel


class OrderDTO(BaseModel):
    id: UUID
    price: Decimal
    description: str


class OrderItemCreatedDTO(BaseModel):
    title: str
    unit_price: Decimal
    quantity: int


class OrderCreatedDTO(BaseModel):
    entity_id: UUID
    price: Decimal
    description: str
    items: list[OrderItemCreatedDTO]
    user_id: int
    email: str
