from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.analytics.dto import UserCreatedAnalyticDTO
from src.infrastructure.sqlalchemy.analytics.model import UserActionAnalyticORM


class UserActionAnalyticRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(
            self, dto: UserCreatedAnalyticDTO
    ):
        analytic_orm = UserActionAnalyticORM(
            user_id=dto.entity_id,
            action=dto.event_type,

        )
        self._session.add(analytic_orm)

    async def get_total_action_count(
            self
    ) -> int:
        return (await self._session.execute(
            select(func.count())
            .select_from(UserActionAnalyticORM)
        )).scalar()
