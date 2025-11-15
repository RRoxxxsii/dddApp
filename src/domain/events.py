import uuid
from dataclasses import dataclass, fields, is_dataclass
from datetime import datetime
from typing import Any


@dataclass
class DomainEvent:
    entity_id: str | int | uuid.UUID | None
    event_type: str
    event_id = uuid.uuid4()
    occurred_at = datetime.now()
    event_version = "1.0"

    def dict(self) -> dict:
        result = {}

        result["event_id"] = str(self.event_id)
        result["occurred_at"] = self.occurred_at.isoformat()
        result["event_version"] = self.event_version
        result["event_type"] = self.event_type

        if is_dataclass(self):
            for field in fields(self):
                if field.name in [
                    "event_id",
                    "occurred_at",
                    "event_version",
                    "event_type",
                ]:
                    continue

                value = getattr(self, field.name)
                result[field.name] = self._convert_value(value)

        return result

    def _convert_value(self, value: Any) -> Any:
        if value is None:
            return None
        elif is_dataclass(value):
            return value.dict()
        elif hasattr(value, "dict") and callable(getattr(value, "dict")):
            return value.dict()
        elif isinstance(value, (datetime, uuid.UUID)):
            return str(value)
        elif isinstance(value, list):
            return [self._convert_value(item) for item in value]
        elif isinstance(value, dict):
            return {
                key: self._convert_value(val) for key, val in value.items()
            }
        else:
            return value
