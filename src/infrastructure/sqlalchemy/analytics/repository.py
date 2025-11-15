from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.ports.repositories import ABCUserActionAnalyticRepository
from src.application.usecases.analytics.dto import UserCreatedDTO
from src.infrastructure.sqlalchemy.analytics.model import UserActionAnalyticORM


class UserActionAnalyticRepository(ABCUserActionAnalyticRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, dto: UserCreatedDTO) -> None:
        analytic_orm = UserActionAnalyticORM(
            user_id=dto.entity_id,
            action=dto.event_type,
        )
        self._session.add(analytic_orm)

    async def get_total_action_count(self) -> int:
        return (
            await self._session.execute(
                select(func.count()).select_from(UserActionAnalyticORM)
            )
        ).scalar()
