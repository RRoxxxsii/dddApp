from abc import ABC, abstractmethod

from src.infrastructure.sqlalchemy.uow import UnitOfWork


class BaseUseCase(ABC):
    def __init__(self, uow: UnitOfWork):
        self._uow = uow

    @abstractmethod
    async def __call__(self, *args, **kwargs):
        raise NotImplementedError
