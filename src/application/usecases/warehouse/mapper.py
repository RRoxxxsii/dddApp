from src.application.usecases.warehouse.dto import ProductDTO
from src.domain.warehouse.entities import Product


class WarehouseMapper:
    @staticmethod
    def map_product(product: Product) -> ProductDTO:
        return ProductDTO(
            id=product.id,
            price=product.price,
            title=product.title,
            description=product.description,
        )

    @staticmethod
    def map_many_products(products: list[Product]) -> list[ProductDTO]:
        return [
            ProductDTO(
                id=product.id,
                price=product.price,
                title=product.title,
                description=product.description,
            )
            for product in products
        ]
