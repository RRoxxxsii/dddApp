import asyncio
from contextlib import asynccontextmanager

from fastapi import APIRouter, FastAPI

from src.config import get_settings
from src.infrastructure.broker.consumer import ModularKafkaConsumer
from src.infrastructure.broker.event_bus.config import build_event_bus
from src.infrastructure.broker.main import setup_kafka_consumers
from src.infrastructure.broker.outbox_processor import OutboxProcessor
from src.infrastructure.broker.producer import AIOKafkaProducer
from src.infrastructure.sqlalchemy.main import (
    create_async_engine,
    create_async_pool,
)
from src.presentation.api.analytics.router import router as analytics_router
from src.presentation.api.exception_handlers import setup_exception_handlers
from src.presentation.api.orders.router import router as orders_router
from src.presentation.api.users.router import router as users_router
from src.presentation.di import get_db_session, get_event_bus
from src.presentation.providers import DBProvider


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    producer = AIOKafkaProducer(bootstrap_servers=settings.bootstrap_servers)
    event_bus = build_event_bus(producer)

    engine = create_async_engine(config=settings)
    pool = create_async_pool(engine=engine)
    db_provider = DBProvider(pool)

    outbox_processor = OutboxProcessor(
        db_provider.provide_client, producer=producer
    )

    consumer_configs = setup_kafka_consumers(db_provider)

    consumer_tasks = []
    for consumer, topic_handlers in consumer_configs:
        modular_consumer = ModularKafkaConsumer(
            name=consumer.config.group_id,
            config=consumer.config,
            topic_handlers=topic_handlers,
        )
        task = asyncio.create_task(modular_consumer.consume())
        consumer_tasks.append(task)

    outbox_task = asyncio.create_task(outbox_processor.start_processing())

    await producer.start()

    app.dependency_overrides[get_event_bus] = lambda: event_bus
    app.dependency_overrides[get_db_session] = db_provider.provide_client

    yield

    for task in consumer_tasks:
        task.cancel()

    outbox_task.cancel()

    if consumer_tasks:
        await asyncio.gather(*consumer_tasks, return_exceptions=True)

    await producer.stop()
    await engine.dispose()


def build_routers(app: FastAPI):
    v1_router = APIRouter(prefix="/v1")
    v1_router.include_router(users_router, prefix="/api/users", tags=["Users"])
    v1_router.include_router(
        analytics_router, prefix="/api/analytics", tags=["Analytics"]
    )
    v1_router.include_router(
        orders_router, prefix="/api/orders", tags=["Orders"]
    )

    app.include_router(v1_router, prefix="")


def build_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)

    build_routers(app)
    setup_exception_handlers(app)

    return app
