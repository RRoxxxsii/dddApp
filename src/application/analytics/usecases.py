from src.application.analytics.dto import UserCreatedAnalyticDTO
from src.domain.usecase import BaseUseCase
from src.infrastructure.sqlalchemy.uow import UnitOfWork


class CreateUserActionAnalyticUseCase(BaseUseCase):

    async def __call__(self, dto: UserCreatedAnalyticDTO) -> None:
        await self._uow.user_analytics_repository.create(dto)
        await self._uow.commit()


class GetUserActionCountUseCase(BaseUseCase):

    async def __call__(self) -> int:
        return await self._uow.user_analytics_repository.get_total_action_count()


class UserActionAnalyticInteractor:
    def __init__(self, uow: UnitOfWork):
        self._uow = uow

    async def create_user_action_analytic(self, dto: UserCreatedAnalyticDTO) -> None:
        return await CreateUserActionAnalyticUseCase(self._uow)(dto)

    async def get_user_action_count(self) -> int:
        return await GetUserActionCountUseCase(self._uow)()
