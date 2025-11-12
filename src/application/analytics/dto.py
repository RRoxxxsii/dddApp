from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class UserCreatedDTO(BaseModel):
    event_id: UUID
    entity_id: int
    email: str
    first_name: str
    last_name: str
    occurred_at: datetime
    event_version: str
    event_type: str
