import traceback
from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import Any

from src.application.ports.mailing import ABCNotificationClient
from src.application.usecases.analytics.usecases import (
    CreateUserActionAnalyticUseCase,
)
from src.application.usecases.notifications.usecases import (
    SendGreetingEmailUseCase,
    SendOrderCreatedNotificationUseCase,
)
from src.domain.usecase import BaseUseCase
from src.infrastructure.broker.dto_factory import ABCDTOFactory
from src.infrastructure.sqlalchemy.uow import UnitOfWork
from src.presentation.services import build_repository_handler


class ABCHandler(ABC):
    def __init__(
        self,
        dto_factory: ABCDTOFactory,
        use_case_factories: list[Callable[[UnitOfWork], BaseUseCase]],
        uow_provider: Callable,
    ):
        self.use_case_factories = use_case_factories
        self.uow_provider = uow_provider
        self.dto_factory = dto_factory

    @abstractmethod
    async def handle(self, raw_message: dict) -> None:
        raise NotImplementedError


class UseCaseFactory:
    def __init__(
        self,
        notification_client: ABCNotificationClient,
    ):
        self._notification_client = notification_client

    def create_send_greeting_email(
        self, db_session: Any
    ) -> SendGreetingEmailUseCase:
        return SendGreetingEmailUseCase(
            UnitOfWork(db_session),
            self._notification_client,
            build_repository_handler(db_session),
        )

    def create_send_order_created_email(
        self, db_session: Any
    ) -> SendOrderCreatedNotificationUseCase:
        return SendOrderCreatedNotificationUseCase(
            UnitOfWork(db_session),
            self._notification_client,
            build_repository_handler(db_session),
        )

    def create_user_analytics(
        self, db_session: Any
    ) -> CreateUserActionAnalyticUseCase:
        return CreateUserActionAnalyticUseCase(
            UnitOfWork(db_session), build_repository_handler(db_session)
        )


class EventMultiHandler(ABCHandler):
    def __init__(
        self,
        use_case_factories: list[Callable[[UnitOfWork], BaseUseCase]],
        uow_provider: Callable,
        dto_factory: ABCDTOFactory,
    ):
        super().__init__(
            use_case_factories=use_case_factories,
            uow_provider=uow_provider,
            dto_factory=dto_factory,
        )
        self.use_case_factories = use_case_factories
        self.uow_provider = uow_provider

    async def handle(self, raw_message: dict) -> None:
        try:
            async for uow in self.uow_provider():
                for factory in self.use_case_factories:
                    use_case = factory(uow)
                    dto = self.dto_factory.execute(raw_message)
                    try:
                        await use_case(dto)
                    except Exception as e:  # noqa
                        traceback.print_exc()

                await uow.commit()
                break
        except Exception as e:  # noqa
            traceback.print_exc()
