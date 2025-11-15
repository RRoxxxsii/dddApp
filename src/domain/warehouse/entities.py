from dataclasses import dataclass

from src.domain.entities import BaseEntity
from src.domain.warehouse.valueobjects import Money, ProductId


@dataclass
class Product(BaseEntity):
    id: ProductId

    price: Money
    title: str
    description: str
