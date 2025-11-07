from src.domain.users.events import UserRegisteredEvent
from src.infrastructure.broker.event_bus.main import EventBus
from src.infrastructure.broker.producer import AIOKafkaProducer


def build_event_bus(broker: AIOKafkaProducer) -> EventBus:
    event_bus = EventBus(
        broker=broker, mapper={UserRegisteredEvent: ("users", "prefix")}
    )

    return event_bus
