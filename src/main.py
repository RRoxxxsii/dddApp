import asyncio
from contextlib import asynccontextmanager

from fastapi import APIRouter, FastAPI

from src.config import get_settings
from src.infrastructure.broker.consumer import (
    KafkaConfig,
    KafkaMessageConsumer,
)
from src.infrastructure.broker.dto_factory import UserCreatedDTOFactory
from src.infrastructure.broker.event_bus.config import build_event_bus
from src.infrastructure.broker.handlers import UserCreatedMultiHandler, UseCaseFactory
from src.infrastructure.broker.producer import AIOKafkaProducer
from src.infrastructure.mailing.client import ConsoleMailingClient
from src.infrastructure.sqlalchemy.main import (
    create_async_engine,
    create_async_pool,
)
from src.presentation.api.analytics.router import router as analytics_router
from src.presentation.api.exception_handlers import setup_exception_handlers
from src.presentation.api.users.router import router as users_router
from src.presentation.di import get_event_bus, get_uow
from src.presentation.providers import DBProvider


def setup_kafka_analytics_consumer(db_provider: DBProvider):
    kafka_config = KafkaConfig(
        bootstrap_servers="kafka:9092",
        group_id="analytics-service",
        auto_offset_reset="earliest",
    )

    dto_factory = UserCreatedDTOFactory()

    use_case_factory = UseCaseFactory(notification_client=ConsoleMailingClient())
    user_created_multi_handler = UserCreatedMultiHandler(
        use_case_factories=[
            use_case_factory.create_user_analytics,
            use_case_factory.create_send_greeting_email,
        ],
        uow_provider=db_provider.provide_client,
        dto_factory=dto_factory
    )

    consumer = KafkaMessageConsumer(kafka_config)

    topic_handlers = {
        "user.created": user_created_multi_handler
    }

    return consumer, topic_handlers


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    producer = AIOKafkaProducer(bootstrap_servers="kafka:9092")
    event_bus = build_event_bus(producer)

    engine = create_async_engine(config=settings)
    pool = create_async_pool(engine=engine)

    db_provider = DBProvider(pool)

    consumer, topic_handlers = setup_kafka_analytics_consumer(db_provider)

    consumer_task = asyncio.create_task(consumer.consume(topic_handlers))

    await producer.start()

    app.dependency_overrides[get_event_bus] = lambda: event_bus  # noqa
    app.dependency_overrides[get_uow] = db_provider.provide_client  # noqa

    yield

    consumer_task.cancel()
    try:
        await consumer_task
    except asyncio.CancelledError:
        pass

    await producer.stop()
    await engine.dispose()
    await consumer.stop()


def build_routers(app: FastAPI):
    v1_router = APIRouter(prefix="/v1")
    v1_router.include_router(users_router, prefix="/api/users", tags=["Users"])
    v1_router.include_router(
        analytics_router, prefix="/api/analytics", tags=["Analytics"]
    )

    app.include_router(v1_router, prefix="")


def build_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)

    build_routers(app)
    setup_exception_handlers(app)

    return app
