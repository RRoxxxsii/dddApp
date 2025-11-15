from src.application.ports.event_bus import ABCEventBus
from src.application.ports.repositories import RepositoryHandler
from src.application.usecases.users.dto import UserDTO
from src.application.usecases.users.mapper import UserMapper
from src.domain.exceptions import AlreadyExistsException
from src.domain.usecase import BaseUseCase
from src.domain.users.entities import User
from src.infrastructure.sqlalchemy.exceptions import (
    RepositoryAlreadyExistsException,
)
from src.infrastructure.sqlalchemy.uow import UnitOfWork
from src.presentation.api.users.schema import CreateUser


class CreateUserUseCase(BaseUseCase):
    def __init__(
        self,
        uow: UnitOfWork,
        event_bus: ABCEventBus,
        repository_handler: RepositoryHandler,
    ) -> None:
        super().__init__(uow=uow, repository_handler=repository_handler)
        self._event_bus = event_bus
        self._mapper = UserMapper
        self._repository_handler = repository_handler

    async def __call__(self, dto: CreateUser) -> UserDTO:
        user = User.create(
            first_name=dto.first_name,
            last_name=dto.last_name,
            password=dto.password,
            email=dto.email,
        )

        try:
            await self._repository_handler.user_repo.create(user)
        except RepositoryAlreadyExistsException:
            await self._uow.rollback()
            raise AlreadyExistsException(
                message=f"User with {dto.email} already exists"
            )

        user.assign_id(user_id=user.id)
        events = user.clear_domain_events()

        await self._uow.commit()
        await self._event_bus.publish_many(events)

        return self._mapper.map_user(user)


class UserInteractor:
    def __init__(
        self,
        uow: UnitOfWork,
        event_bus: ABCEventBus,
        repository_handler: RepositoryHandler,
    ) -> None:
        self._uow = uow
        self._event_bus = event_bus
        self._repository_handler = repository_handler

    async def create_user(
        self,
        dto: CreateUser,
    ) -> UserDTO:
        return await CreateUserUseCase(
            self._uow, self._event_bus, self._repository_handler
        )(dto)
