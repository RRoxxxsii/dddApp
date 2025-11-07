from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class BaseId:
    value: str | int | UUID
