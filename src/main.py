from contextlib import asynccontextmanager

from fastapi import APIRouter, FastAPI

from src.config import get_settings
from src.infrastructure.broker.event_bus.config import build_event_bus
from src.infrastructure.broker.producer import AIOKafkaProducer
from src.infrastructure.sqlalchemy.main import (
    create_async_engine,
    create_async_pool,
)
from src.presentation.api.exception_handlers import setup_exception_handlers
from src.presentation.api.users.router import router as users_router
from src.presentation.di import get_event_bus, get_uow
from src.presentation.providers import DBProvider


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    producer = AIOKafkaProducer(bootstrap_servers="kafka:9092")
    event_bus = build_event_bus(producer)

    engine = create_async_engine(config=settings)
    pool = create_async_pool(engine=engine)

    db_provider = DBProvider(pool)

    await producer.start()

    app.dependency_overrides[get_event_bus] = lambda: event_bus  # noqa
    app.dependency_overrides[get_uow] = db_provider.provide_client  # noqa

    yield

    await producer.stop()
    await engine.dispose()


def build_routers(app: FastAPI):
    v1_router = APIRouter(prefix="/v1")
    v1_router.include_router(users_router, prefix="/api/users", tags=["Users"])

    app.include_router(v1_router, prefix="")


def build_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)

    build_routers(app)
    setup_exception_handlers(app)

    return app
