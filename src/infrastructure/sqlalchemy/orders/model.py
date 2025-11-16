from decimal import Decimal
from uuid import UUID

from sqlalchemy import DECIMAL
from sqlalchemy import UUID as SA_UUID
from sqlalchemy import BigInteger, ForeignKey, SmallInteger, String
from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.sqlalchemy import Base, bigint_pk, time_created


class OrderItemORM(Base):
    __tablename__ = "order_items"

    id: Mapped[bigint_pk]
    order_id: Mapped[UUID] = mapped_column(
        SA_UUID,
        ForeignKey("orders.id"),
        nullable=False,
    )

    product_id: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
    )
    quantity: Mapped[int] = mapped_column(
        SmallInteger,
        nullable=False,
    )


class OrderORM(Base):
    __tablename__ = "orders"

    id: Mapped[UUID] = mapped_column(SA_UUID, nullable=False, primary_key=True)
    price: Mapped[Decimal] = mapped_column(
        DECIMAL,
        nullable=False,
    )
    user_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    description: Mapped[String] = mapped_column(
        String,
        nullable=False,
    )

    created_at: Mapped[time_created]
