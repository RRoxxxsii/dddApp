from sqlalchemy.orm import Mapped

from src.infrastructure.sqlalchemy.model import Base, bigint_pk


class UserORM(Base):
    __tablename__ = "users"

    id: Mapped[bigint_pk]
    first_name: Mapped[str]
    last_name: Mapped[str]
    email: Mapped[str]
    hashed_password: Mapped[str]
