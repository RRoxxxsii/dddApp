from abc import ABC, abstractmethod

from src.domain.events import DomainEvent
from src.infrastructure.broker.producer import ABCProducer


class ABCEventBus(ABC):
    def __init__(
        self,
        broker: ABCProducer,
    ):
        self._broker = broker

    @abstractmethod
    async def publish_one(self, event: DomainEvent) -> None:
        raise NotImplementedError

    @abstractmethod
    async def publish_many(self, events: list[DomainEvent]) -> None:
        raise NotImplementedError
