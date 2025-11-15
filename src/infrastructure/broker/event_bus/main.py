from src.application.ports.event_bus import ABCEventBus
from src.domain.events import DomainEvent
from src.infrastructure.broker.producer import ABCProducer


class EventBus(ABCEventBus):
    def __init__(
        self,
        broker: ABCProducer,
        mapper: dict[type[DomainEvent], tuple[str, str]],
    ):
        super().__init__(broker)
        self._mapper = mapper

    async def _publish_one(self, event: DomainEvent):
        event_type = type(event)

        topic, prefix = self._mapper[event_type]
        key = f"{prefix}_{event.entity_id}"
        await self._broker.send(topic=topic, key=key, value=event.dict())

    async def publish_many(self, events: list[DomainEvent]):
        for event in events:
            await self._publish_one(event)

    async def publish_one(self, event: DomainEvent):
        await self._publish_one(event)
