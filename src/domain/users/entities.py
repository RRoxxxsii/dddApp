from dataclasses import dataclass

from src.domain.analytics.entity import ActionTypeEnum
from src.domain.entities import BaseEntity
from src.domain.users.events import UserRegisteredEvent
from src.domain.users.valueobjects import Email, Password, UserId


@dataclass
class User(BaseEntity):
    id: UserId | None
    first_name: str
    last_name: str
    email: Email
    hashed_password: str

    @classmethod
    def create(
        cls,
        first_name: str,
        last_name: str,
        email: str,
        password: str,
    ) -> "User":
        password_: Password = Password(password)
        hashed_password = password_.hash_password()

        user = User(
            id=None,
            first_name=first_name,
            last_name=last_name,
            email=Email(email),
            hashed_password=hashed_password,
            _domain_events=list(),
        )

        event = UserRegisteredEvent(
            entity_id=user.id.value if user.id else None,
            email=user.email.value,
            first_name=user.first_name,
            last_name=user.last_name,
            event_type=ActionTypeEnum.USER_CREATED.value,
        )
        user._add_domain_event(event)

        return user

    def assign_id(self, user_id: UserId) -> None:
        self.id = user_id
        for event in self._domain_events:
            event.entity_id = user_id.value
