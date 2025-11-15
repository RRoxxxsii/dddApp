from src.config import get_settings
from src.infrastructure.broker.consumer import (
    KafkaConfig,
    KafkaMessageConsumer,
)
from src.infrastructure.broker.dto_factory import (
    OrderCreatedFactory,
    UserCreatedDTOFactory,
)
from src.infrastructure.broker.handlers import (
    EventMultiHandler,
    UseCaseFactory,
)
from src.infrastructure.mailing.client import ConsoleMailingClient
from src.presentation.providers import DBProvider


def setup_kafka_consumers(db_provider: DBProvider):
    use_case_factory = UseCaseFactory(
        notification_client=ConsoleMailingClient()
    )

    analytics_consumer = create_analytics_consumer(
        db_provider, use_case_factory
    )
    notifications_consumer = create_notifications_consumer(
        db_provider, use_case_factory
    )

    return [analytics_consumer, notifications_consumer]


def create_analytics_consumer(
    db_provider: DBProvider, use_case_factory: UseCaseFactory
):
    settings = get_settings()

    kafka_config = KafkaConfig(
        bootstrap_servers=settings.bootstrap_servers,
        group_id="analytics-module",
        auto_offset_reset="earliest",
    )

    user_created_handler = EventMultiHandler(
        use_case_factories=[
            use_case_factory.create_user_analytics,
        ],
        uow_provider=db_provider.provide_client,
        dto_factory=UserCreatedDTOFactory(),
    )

    consumer = KafkaMessageConsumer(kafka_config)

    topic_handlers = {
        "user.created": user_created_handler,
    }

    return consumer, topic_handlers


def create_notifications_consumer(
    db_provider: DBProvider, use_case_factory: UseCaseFactory
):
    settings = get_settings()
    kafka_config = KafkaConfig(
        bootstrap_servers=settings.bootstrap_servers,
        group_id="notifications-module",
        auto_offset_reset="earliest",
    )

    user_created_handler = EventMultiHandler(
        use_case_factories=[
            use_case_factory.create_send_greeting_email,
        ],
        uow_provider=db_provider.provide_client,
        dto_factory=UserCreatedDTOFactory(),
    )

    order_created_handler = EventMultiHandler(
        use_case_factories=[
            use_case_factory.create_send_order_created_email,
        ],
        uow_provider=db_provider.provide_client,
        dto_factory=OrderCreatedFactory(),
    )

    consumer = KafkaMessageConsumer(kafka_config)

    topic_handlers = {
        "user.created": user_created_handler,
        "order.created": order_created_handler,
    }

    return consumer, topic_handlers
