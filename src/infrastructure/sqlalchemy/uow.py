from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.sqlalchemy.analytics.repository import (
    UserActionAnalyticRepository,
)
from src.infrastructure.sqlalchemy.users.repository import UserRepository


class UnitOfWork:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def __aenter__(self):
        self.user_repository = UserRepository(self._session)
        self.user_analytics_repository = UserActionAnalyticRepository(
            self._session
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            await self._session.rollback()
        await self._session.close()

    async def commit(self):
        await self._session.commit()

    async def rollback(self):
        await self._session.rollback()
