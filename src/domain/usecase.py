from src.application.users.mapper import UserMapper
from src.infrastructure.broker.event_bus.main import ABCEventBus
from src.infrastructure.sqlalchemy.uow import UnitOfWork


class BaseUseCase:
    def __init__(self, uow: UnitOfWork, event_bus: ABCEventBus):
        self._uow = uow
        self._event_bus = event_bus
        self._mapper = UserMapper
