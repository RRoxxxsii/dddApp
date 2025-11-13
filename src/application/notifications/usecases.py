from src.application.analytics.dto import UserCreatedDTO
from src.domain.notifications.valueobjects import EmailTemplate
from src.domain.usecase import BaseUseCase
from src.infrastructure.mailing.client import ABCNotificationClient
from src.infrastructure.sqlalchemy.uow import UnitOfWork


class SendGreetingEmailUseCase(BaseUseCase):
    def __init__(
        self,
        uow: UnitOfWork,
        notification_client: ABCNotificationClient,
    ):
        super().__init__(uow)
        self._notification_client = notification_client

    async def __call__(self, dto: UserCreatedDTO) -> None:
        template = EmailTemplate(
            subject="Hello, $first_name!",
            body="Welcome $first_name $last_name to our service.",
        )

        template_rendered = template.render(**dto.model_dump())

        await self._notification_client.send_message(
            subject=template_rendered.subject,
            body=template_rendered.body,
            email=dto.email,
        )


class NotificationInteractor:
    def __init__(self, uow: UnitOfWork):
        self._uow = uow

    def send_greeting_email(self):
        pass
