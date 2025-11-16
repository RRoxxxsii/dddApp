import datetime
import uuid
from typing import Annotated
from uuid import UUID

from sqlalchemy import JSON
from sqlalchemy import UUID as SA_UUID
from sqlalchemy import BigInteger, Boolean, DateTime, String, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    _repr_cols_num: int = 3
    _repr_cols: tuple = tuple()

    def __repr__(self):
        cols = []
        for idx, col in enumerate(self.__table__.columns.keys()):
            if col in self._repr_cols or idx < self._repr_cols_num:
                cols.append(f"{col}={getattr(self, col)}")
        return f"<{self.__class__.__name__} {', '.join(cols)}>"


bigint_pk = Annotated[
    int,
    mapped_column(BigInteger, primary_key=True, index=True),
]


time_created = Annotated[
    datetime.datetime,
    mapped_column(
        DateTime(timezone=True),
        server_default=func.timezone("Europe/Moscow", func.now()),
    ),
]


class OutboxMessageORM(Base):
    __tablename__ = "outbox_messages"

    id: Mapped[UUID] = mapped_column(
        SA_UUID(as_uuid=True), default=uuid.uuid4, primary_key=True
    )

    aggregate_type: Mapped[str] = mapped_column(String(100), nullable=False)
    aggregate_id: Mapped[str] = mapped_column(String(255), nullable=False)
    event_type: Mapped[str] = mapped_column(String(255), nullable=False)
    payload: Mapped[dict] = mapped_column(JSON, nullable=False)
    is_processed: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False
    )
    created_at: Mapped[time_created]
