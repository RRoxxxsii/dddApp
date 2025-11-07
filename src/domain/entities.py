from dataclasses import dataclass

from src.domain.events import DomainEvent


@dataclass
class BaseEntity:
    _domain_events: list[DomainEvent]

    def _add_domain_event(self, event: DomainEvent) -> None:
        self._domain_events.append(event)

    def clear_domain_events(self) -> list[DomainEvent]:
        events = self._domain_events.copy()
        self._domain_events.clear()
        return events

    @property
    def domain_events(self) -> list[DomainEvent]:
        return self._domain_events.copy()
