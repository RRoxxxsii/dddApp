from abc import ABC, abstractmethod

from src.domain.events import DomainEvent


class EventHandler(ABC):
    @abstractmethod
    async def handle(self, event: DomainEvent) -> None:
        pass

    @property
    @abstractmethod
    def event_type(self) -> type[DomainEvent]:
        pass
