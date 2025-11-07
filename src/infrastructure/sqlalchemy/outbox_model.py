from sqlalchemy import JSON, Boolean, String
from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.sqlalchemy.model import Base, bigint_pk, time_created


class OutboxEventORM(Base):
    __tablename__ = "outbox_events"

    id: Mapped[bigint_pk]
    aggregate_type: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    aggregate_id: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    event_type: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    payload: Mapped[dict] = mapped_column(
        JSON,
        nullable=False,
    )
    processed: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )
    created_at: Mapped[time_created]
