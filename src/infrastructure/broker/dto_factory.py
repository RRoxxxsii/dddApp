from abc import ABC, abstractmethod
from datetime import datetime
from uuid import UUID

from src.application.analytics.dto import UserCreatedDTO


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
            event_type=raw_data["event_type"]
        )
