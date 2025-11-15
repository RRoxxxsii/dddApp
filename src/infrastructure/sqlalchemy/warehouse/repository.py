from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.ports.repositories import ABCWarehouseRepository
from src.domain.warehouse.entities import Product
from src.domain.warehouse.valueobjects import Money, ProductId
from src.infrastructure.sqlalchemy.warehouse.model import ProductORM


class WarehouseRepository(ABCWarehouseRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def _get_product_by_id(self, id_: int) -> ProductORM:
        return (
            await self._session.execute(
                select(ProductORM).where(ProductORM.id == id_)
            )
        ).scalar_one_or_none()

    async def get_many(self, ids: list | None = None) -> list[Product]:
        stmt = select(ProductORM)
        if ids is not None:
            stmt = stmt.where(ProductORM.id.in_(ids))

        products = (await self._session.execute(stmt)).scalars().all()
        return [
            Product(
                id=ProductId(product.id),
                price=Money(product.price),
                title=product.title,
                description=product.description,
                _domain_events=[],
            )
            for product in products
        ]

    async def get_one_by_id(self, id_: int) -> Product:
        product = await self._get_product_by_id(id_)
        return Product(
            id=ProductId(product.id),
            price=Money(product.price),
            title=product.title,
            description=product.description,
            _domain_events=[],
        )
