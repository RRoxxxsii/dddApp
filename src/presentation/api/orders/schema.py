from pydantic import BaseModel


class CreateOrderProductItem(BaseModel):
    product_id: int
    quantity: int


class CreateOrder(BaseModel):
    products: list[CreateOrderProductItem]
    user_id: int
    email: str
