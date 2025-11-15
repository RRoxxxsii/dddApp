import uuid
from dataclasses import dataclass, field
from uuid import UUID

from src.domain.valueobjects import BaseId


@dataclass(frozen=True)
class OrderId(BaseId):
    value: UUID = field(default_factory=uuid.uuid4)
