from dataclasses import dataclass
from typing import ClassVar

from passlib.context import CryptContext

from src.domain.exceptions import ValidationException
from src.domain.users.exceptions import (
    PasswordTooLongException,
    PasswordTooShortException,
)
from src.domain.valueobjects import BaseId

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@dataclass(frozen=True)
class UserId(BaseId):
    value: int


@dataclass(frozen=True)
class Password:
    value: str

    MIN_LENGTH: ClassVar[int] = 8
    MAX_LENGTH: ClassVar[int] = 128

    def __post_init__(self):
        self._validate_length()

    def _validate_length(self) -> None:
        if len(self.value) < self.MIN_LENGTH:
            raise PasswordTooShortException(
                min_length=self.MIN_LENGTH, actual_length=len(self.value)
            )
        if len(self.value) > self.MAX_LENGTH:
            raise PasswordTooLongException(
                max_length=self.MAX_LENGTH, actual_length=len(self.value)
            )

    def hash_password(self) -> str:
        return pwd_context.hash(self.value)

    def verify_password(self, hashed_password: str) -> bool:
        return pwd_context.verify(self.value, hashed_password)


@dataclass(frozen=True)
class Email:
    value: str

    def __post_init__(self):
        if "@" not in self.value:
            raise ValidationException("Invalid email format")

        if len(self.value) > 255:
            raise ValidationException("Email too long")
