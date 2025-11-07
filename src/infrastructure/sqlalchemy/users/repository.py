from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.users.entities import User
from src.domain.users.valueobjects import UserId
from src.infrastructure.sqlalchemy.exceptions import (
    RepositoryAlreadyExistsException,
)
from src.infrastructure.sqlalchemy.users.model import UserORM


class UserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def _get_by_email(self, email: str) -> UserORM | None:
        return (
            await self._session.execute(
                select(UserORM).where(UserORM.email == email)
            )
        ).scalar_one_or_none()

    async def create(self, user: User) -> User:
        user_orm = await self._get_by_email(email=user.email.value)
        if user_orm:
            raise RepositoryAlreadyExistsException

        user_orm = UserORM(
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email.value,
            hashed_password=user.hashed_password,
        )
        self._session.add(user_orm)
        await self._session.flush()
        user.id = UserId(user_orm.id)
        return user
