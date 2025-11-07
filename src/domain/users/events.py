from dataclasses import dataclass
from datetime import datetime
from typing import Any

from src.domain.events import DomainEvent


@dataclass
class UserRegisteredEvent(DomainEvent):
    entity_id: Any | None
    email: str
    first_name: str
    last_name: str
    occurred_at: datetime = None

    def __post_init__(self):
        if self.occurred_at is None:
            self.occurred_at = datetime.now()
