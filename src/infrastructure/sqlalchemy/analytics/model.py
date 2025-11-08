from sqlalchemy import BigInteger, String
from sqlalchemy.orm import Mapped, mapped_column

from src.domain.analytics.entity import ActionTypeEnum
from src.infrastructure.sqlalchemy import Base, bigint_pk
from src.infrastructure.sqlalchemy.model import time_created


class UserActionAnalyticORM(Base):
    __tablename__ = "user_action_analytics"

    id: Mapped[bigint_pk]
    user_id: Mapped[int] = mapped_column(
        BigInteger, nullable=False
    )
    action: Mapped[ActionTypeEnum] = mapped_column(
        String, nullable=False
    )
    created_at: Mapped[time_created]
