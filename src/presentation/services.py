from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.ports.event_bus import ABCEventBus
from src.application.ports.repositories import RepositoryHandler
from src.application.usecases.analytics.usecases import (
    UserActionAnalyticInteractor,
)
from src.application.usecases.orders.usecases import OrderInteractor
from src.application.usecases.users.usecases import UserInteractor
from src.infrastructure.sqlalchemy.analytics.repository import (
    UserActionAnalyticRepository,
)
from src.infrastructure.sqlalchemy.orders.repository import OrderRepository
from src.infrastructure.sqlalchemy.uow import UnitOfWork
from src.infrastructure.sqlalchemy.users.repository import UserRepository
from src.infrastructure.sqlalchemy.warehouse.repository import (
    WarehouseRepository,
)
from src.presentation.di import get_db_session, get_event_bus


def build_repository_handler(session: AsyncSession) -> RepositoryHandler:
    return RepositoryHandler(
        user_repository=UserRepository(session),
        user_analytics_repo=UserActionAnalyticRepository(session),
        warehouse_repository=WarehouseRepository(session),
        order_repository=OrderRepository(session),
    )


def get_user_interactor(
    db_session: AsyncSession = Depends(get_db_session),
    event_bus: ABCEventBus = Depends(get_event_bus),
) -> UserInteractor:
    uow = UnitOfWork(db_session)
    return UserInteractor(
        uow=uow,
        event_bus=event_bus,
        repository_handler=build_repository_handler(db_session),
    )


def get_user_action_interactor(
    db_session: AsyncSession = Depends(get_db_session),
) -> UserActionAnalyticInteractor:
    uow = UnitOfWork(db_session)
    return UserActionAnalyticInteractor(
        uow=uow,
        repository_handler=build_repository_handler(db_session),
    )


def get_order_interactor(
    db_session: AsyncSession = Depends(get_db_session),
    event_bus: ABCEventBus = Depends(get_event_bus),
):
    uow = UnitOfWork(db_session)
    return OrderInteractor(
        uow=uow,
        repository_handler=build_repository_handler(db_session),
        event_bus=event_bus,
    )
