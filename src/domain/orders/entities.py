from dataclasses import dataclass

from src.domain.entities import BaseEntity
from src.domain.warehouse.valueobjects import Money, ProductId


@dataclass
class OrderItem(BaseEntity):
    product_id: ProductId
    quantity: int
    unit_price: Money
    title: str

    @classmethod
    def create(
        cls,
        product_id: ProductId,
        quantity: int,
        unit_price: Money,
        title: str,
    ) -> "OrderItem":
        return OrderItem(
            product_id=product_id,
            quantity=quantity,
            unit_price=unit_price,
            title=title,
            _domain_events=list(),
        )
