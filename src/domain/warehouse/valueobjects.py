from dataclasses import dataclass
from decimal import Decimal

from src.domain.valueobjects import BaseId
from src.domain.warehouse.exceptions import MoneyException


@dataclass(frozen=True)
class ProductId(BaseId):
    value: int


@dataclass(frozen=True)
class Money:
    amount: Decimal
    currency: str = "RUB"

    def __post_init__(self):
        if self.amount < 0:
            raise MoneyException("Money amount cannot be negative")
        if not self.currency:
            raise MoneyException("Currency cannot be empty")

    def __add__(self, other: "Money") -> "Money":
        if self.currency != other.currency:
            raise MoneyException("Cannot add different currencies")
        return Money(self.amount + other.amount, self.currency)

    def __sub__(self, other: "Money") -> "Money":
        if self.currency != other.currency:
            raise MoneyException("Cannot subtract different currencies")
        return Money(self.amount - other.amount, self.currency)

    def __mul__(self, multiplier: Decimal) -> "Money":
        return Money(self.amount * multiplier, self.currency)

    def __str__(self) -> str:
        return f"{self.currency} {self.amount:.2f}"  # noqa
