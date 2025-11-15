import asyncio
from contextlib import asynccontextmanager

from fastapi import APIRouter, FastAPI

from src.config import get_settings
from src.infrastructure.broker.event_bus.config import build_event_bus
from src.infrastructure.broker.main import setup_kafka_analytics_consumer
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

    consumer, topic_handlers = setup_kafka_analytics_consumer(db_provider)

    consumer_task = asyncio.create_task(consumer.consume(topic_handlers))

    await producer.start()

    app.dependency_overrides[get_event_bus] = lambda: event_bus  # noqa
    app.dependency_overrides[
        get_db_session
    ] = db_provider.provide_client  # noqa

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
    v1_router.include_router(
        orders_router, prefix="/api/orders", tags=["Orders"]
    )

    app.include_router(v1_router, prefix="")


def build_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)

    build_routers(app)
    setup_exception_handlers(app)

    return app
