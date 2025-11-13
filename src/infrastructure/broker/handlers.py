import traceback
from abc import ABC, abstractmethod
from collections.abc import Callable

from src.application.analytics.usecases import CreateUserActionAnalyticUseCase
from src.application.notifications.usecases import SendGreetingEmailUseCase
from src.domain.usecase import BaseUseCase
from src.infrastructure.broker.dto_factory import ABCDTOFactory
from src.infrastructure.mailing.client import ABCNotificationClient
from src.infrastructure.sqlalchemy.uow import UnitOfWork


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
        self, uow: UnitOfWork
    ) -> SendGreetingEmailUseCase:
        return SendGreetingEmailUseCase(uow, self._notification_client)

    def create_user_analytics(
        self, uow: UnitOfWork
    ) -> CreateUserActionAnalyticUseCase:
        return CreateUserActionAnalyticUseCase(uow)


class UserCreatedMultiHandler(ABCHandler):
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
