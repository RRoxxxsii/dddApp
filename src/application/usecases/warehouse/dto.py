from decimal import Decimal

from pydantic import BaseModel


class ProductDTO(BaseModel):
    id: int
    price: Decimal
    title: str
    description: str
