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


def setup_kafka_analytics_consumer(db_provider: DBProvider):
    settings = get_settings()
    kafka_config = KafkaConfig(
        bootstrap_servers=settings.bootstrap_servers,
        group_id="analytics-service",
        auto_offset_reset="earliest",
    )

    use_case_factory = UseCaseFactory(
        notification_client=ConsoleMailingClient()
    )
    user_created_multi_handler = EventMultiHandler(
        use_case_factories=[
            use_case_factory.create_user_analytics,
            use_case_factory.create_send_greeting_email,
        ],
        uow_provider=db_provider.provide_client,
        dto_factory=UserCreatedDTOFactory(),
    )
    order_created_multi_handler = EventMultiHandler(
        use_case_factories=[
            use_case_factory.create_send_order_created_email,
        ],
        uow_provider=db_provider.provide_client,
        dto_factory=OrderCreatedFactory(),
    )

    consumer = KafkaMessageConsumer(kafka_config)

    topic_handlers = {
        "user.created": user_created_multi_handler,
        "order.created": order_created_multi_handler,
    }

    return consumer, topic_handlers
