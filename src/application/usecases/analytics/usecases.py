from src.application.ports.repositories import RepositoryHandler
from src.application.usecases.analytics.dto import UserCreatedDTO
from src.domain.usecase import BaseUseCase
from src.infrastructure.sqlalchemy.uow import UnitOfWork


class CreateUserActionAnalyticUseCase(BaseUseCase):
    def __init__(
        self,
        uow: UnitOfWork,
        repository_handler: RepositoryHandler,
    ) -> None:
        super().__init__(uow=uow, repository_handler=repository_handler)
        self._repository_handler = repository_handler

    async def __call__(self, dto: UserCreatedDTO) -> None:
        await self._repository_handler.user_analytics_repo.create(dto)
        await self._uow.commit()


class GetUserActionCountUseCase(BaseUseCase):
    async def __call__(self) -> int:
        return (
            await self._repository_handler.user_analytics_repo.get_total_action_count()  # noqa
        )


class UserActionAnalyticInteractor:
    def __init__(
        self,
        uow: UnitOfWork,
        repository_handler: RepositoryHandler,
    ) -> None:
        self._uow = uow
        self._repository_handler = repository_handler

    async def create_user_action_analytic(self, dto: UserCreatedDTO) -> None:
        return await CreateUserActionAnalyticUseCase(
            self._uow,
            self._repository_handler,
        )(dto)

    async def get_user_action_count(self) -> int:
        return await GetUserActionCountUseCase(
            self._uow,
            self._repository_handler,
        )()
