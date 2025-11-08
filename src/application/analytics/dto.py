from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class UserCreatedAnalyticDTO:
    event_id: UUID
    entity_id: int
    email: str
    first_name: str
    last_name: str
    occurred_at: datetime
    event_version: str
    event_type: str
