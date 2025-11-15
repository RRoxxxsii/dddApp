from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker


class DBProvider:
    def __init__(self, pool: async_sessionmaker[AsyncSession]):
        self.pool = pool

    async def provide_client(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.pool() as session:
            async with session:
                yield session
