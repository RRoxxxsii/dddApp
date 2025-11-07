from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.infrastructure.sqlalchemy.uow import UnitOfWork


class DBProvider:
    def __init__(self, pool: async_sessionmaker[AsyncSession]):
        self.pool = pool

    async def provide_client(self) -> AsyncGenerator[UnitOfWork, None]:
        async with self.pool() as session:
            async with UnitOfWork(session) as uow:
                yield uow
