from src.application.ports.repositories import RepositoryHandler
from src.application.usecases.warehouse.dto import ProductDTO
from src.application.usecases.warehouse.mapper import WarehouseMapper
from src.domain.usecase import BaseUseCase
from src.infrastructure.sqlalchemy.uow import UnitOfWork


class GetProductsUseCase(BaseUseCase):
    def __init__(
        self,
        uow: UnitOfWork,
        repository_handler: RepositoryHandler,
    ) -> None:
        super().__init__(uow=uow, repository_handler=repository_handler)
        self._repository_handler = repository_handler
        self._mapper = WarehouseMapper

    async def __call__(self) -> list[ProductDTO]:
        products = await self._repository_handler.warehouse_repo.get_many()
        return self._mapper.map_many_products(products)


class GetProductByIdUseCase(BaseUseCase):
    def __init__(
        self,
        uow: UnitOfWork,
        repository_handler: RepositoryHandler,
    ) -> None:
        super().__init__(uow=uow, repository_handler=repository_handler)
        self._repository_handler = repository_handler
        self._mapper = WarehouseMapper

    async def __call__(self, id_: int) -> ProductDTO:
        product = await self._repository_handler.warehouse_repo.get_one_by_id(
            id_=id_
        )
        return self._mapper.map_product(product)


class WarehouseInteractor:
    def __init__(
        self,
        uow: UnitOfWork,
        repository_handler: RepositoryHandler,
    ) -> None:
        self._uow = uow
        self._repository_handler = repository_handler

    async def get_products(self) -> list[ProductDTO]:
        return await GetProductsUseCase(self._uow, self._repository_handler)()

    async def get_products_by_id(self, product_id: int) -> ProductDTO:
        return await GetProductByIdUseCase(
            self._uow, self._repository_handler
        )(product_id)
