import traceback
from abc import ABC, abstractmethod
from typing import Callable, AsyncGenerator

from src.application.analytics.usecases import CreateUserActionAnalyticUseCase
from src.infrastructure.broker.dto_factory import ABCDTOFactory
from src.infrastructure.sqlalchemy.uow import UnitOfWork


class ABCHandler(ABC):
    def __init__(self, uow_provider: Callable[[], AsyncGenerator[UnitOfWork, None]], dto_factory: ABCDTOFactory):
        self.uow_provider = uow_provider
        self.dto_factory = dto_factory

    @abstractmethod
    async def handle(self, raw_message: dict) -> None:
        raise NotImplementedError


class UserCreatedHandler(ABCHandler):

    async def handle(self, raw_message: dict) -> None:
        try:
            dto = self.dto_factory.execute(raw_message)

            async for uow in self.uow_provider():
                use_case = CreateUserActionAnalyticUseCase(uow)
                await use_case(dto)
                break

        except Exception as e:
            traceback.print_exc()
