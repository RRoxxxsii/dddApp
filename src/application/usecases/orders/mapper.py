from src.application.usecases.orders.dto import OrderDTO
from src.domain.orders.aggregates import Order


class OrderMapper:
    @staticmethod
    def map_order(order: Order) -> OrderDTO:
        return OrderDTO(
            id=order.id.value,
            description=order.description,
            price=order.price.amount,
        )
