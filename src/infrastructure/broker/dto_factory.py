from abc import ABC, abstractmethod
from datetime import datetime
from decimal import Decimal
from uuid import UUID

from src.application.usecases.analytics.dto import UserCreatedDTO
from src.application.usecases.orders.dto import (
    OrderCreatedDTO,
    OrderItemCreatedDTO,
)


class ABCDTOFactory(ABC):
    @staticmethod
    @abstractmethod
    def execute(raw_data: dict):
        raise NotImplementedError


class UserCreatedDTOFactory(ABCDTOFactory):
    @staticmethod
    def execute(raw_data: dict) -> UserCreatedDTO:
        return UserCreatedDTO(
            event_id=UUID(raw_data["event_id"]),
            entity_id=raw_data["entity_id"],
            email=raw_data["email"],
            first_name=raw_data["first_name"],
            last_name=raw_data["last_name"],
            occurred_at=datetime.fromisoformat(raw_data["occurred_at"]),
            event_version=raw_data["event_version"],
            event_type=raw_data["event_type"],
        )


class OrderCreatedFactory(ABCDTOFactory):
    @staticmethod
    def execute(raw_data: dict) -> OrderCreatedDTO:
        return OrderCreatedDTO(
            entity_id=UUID(raw_data["entity_id"]),
            price=Decimal(raw_data["price"]),
            description=raw_data["description"],
            user_id=int(raw_data["user_id"]),
            email=raw_data["email"],
            items=[
                OrderItemCreatedDTO(
                    title=item["title"],
                    unit_price=Decimal(item["unit_price"]),
                    quantity=int(item["quantity"]),
                )
                for item in raw_data["items"]
            ],
        )
