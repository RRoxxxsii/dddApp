import uuid
from dataclasses import dataclass, fields
from datetime import datetime


@dataclass
class DomainEvent:
    entity_id: str | int | uuid.UUID | None
    event_id = uuid.uuid4()
    occurred_at = datetime.now()
    event_version = "1.0"

    @property
    def event_type(self) -> str:
        return self.__class__.__name__

    def dict(self) -> dict:
        result = dict()

        result["event_id"] = str(self.event_id)
        result["occurred_at"] = self.occurred_at.isoformat()
        result["event_version"] = self.event_version
        result["event_type"] = self.event_type

        if hasattr(self, "__dataclass_fields__"):
            for field in fields(self):  # noqa
                value = getattr(self, field.name)
                if hasattr(value, "dict"):
                    result[field.name] = value.dict()
                elif isinstance(value, (datetime, uuid.UUID)):
                    result[field.name] = str(value)
                else:
                    result[field.name] = value

        return result
