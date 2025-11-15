from abc import ABC, abstractmethod

from src.application.ports.repositories import RepositoryHandler
from src.infrastructure.sqlalchemy.uow import UnitOfWork


class BaseUseCase(ABC):
    def __init__(
        self,
        uow: UnitOfWork,
        repository_handler: RepositoryHandler,
    ):
        self._uow = uow
        self._repository_handler = repository_handler

    @abstractmethod
    async def __call__(self, *args, **kwargs):
        raise NotImplementedError
