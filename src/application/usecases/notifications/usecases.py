from src.application.ports.mailing import ABCNotificationClient
from src.application.ports.repositories import RepositoryHandler
from src.application.usecases.analytics.dto import UserCreatedDTO
from src.application.usecases.orders.dto import OrderCreatedDTO
from src.domain.notifications.valueobjects import EmailTemplate
from src.domain.usecase import BaseUseCase
from src.infrastructure.sqlalchemy.uow import UnitOfWork


class SendGreetingEmailUseCase(BaseUseCase):
    def __init__(
        self,
        uow: UnitOfWork,
        notification_client: ABCNotificationClient,
        repository_handler: RepositoryHandler,
    ):
        super().__init__(uow, repository_handler)
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


class SendOrderCreatedNotificationUseCase(BaseUseCase):
    def __init__(
        self,
        uow: UnitOfWork,
        notification_client: ABCNotificationClient,
        repository_handler: RepositoryHandler,
    ):
        super().__init__(uow, repository_handler)
        self._notification_client = notification_client

    async def __call__(self, dto: OrderCreatedDTO) -> None:
        template = EmailTemplate(
            subject="Order created",
            body="Thank you for creating order.",
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
