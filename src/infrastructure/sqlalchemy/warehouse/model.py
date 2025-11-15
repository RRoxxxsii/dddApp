from decimal import Decimal

from sqlalchemy import DECIMAL, String
from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.sqlalchemy import Base, bigint_pk


class ProductORM(Base):
    __tablename__ = "products"

    id: Mapped[bigint_pk]

    price: Mapped[Decimal] = mapped_column(
        DECIMAL,
        nullable=False,
    )
    title: Mapped[String] = mapped_column(
        String,
        nullable=False,
    )
    description: Mapped[String] = mapped_column(
        String,
        nullable=False,
    )
