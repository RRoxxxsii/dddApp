from fastapi import Depends

from src.application.users.usecases import UserInteractor
from src.infrastructure.broker.event_bus.main import ABCEventBus
from src.infrastructure.sqlalchemy.uow import UnitOfWork
from src.presentation.di import get_event_bus, get_uow


def get_user_interactor(
    uow: UnitOfWork = Depends(get_uow),
    event_bus: ABCEventBus = Depends(get_event_bus),
):
    return UserInteractor(uow=uow, event_bus=event_bus)
