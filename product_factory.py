from product import DigitalProduct, PhysicalProduct, Product
from supplier import Supplier


class ProductFactory:
    """Centralises creation of concrete Product objects (Factory pattern)."""

    @staticmethod
    def create(
        product_type: str,
        product_id: str,
        name: str,
        price: float,
        stock_quantity: int,
        supplier: Supplier,
        weight: float = 0.0,
        download_size: float = 0.0,
    ) -> Product:
        """Create and return a Product based on product_type."""
        normalised_type = product_type.strip().lower()
        if normalised_type == "physical":
            return PhysicalProduct(
                product_id, name, price, stock_quantity, supplier, weight
            )
        elif normalised_type == "digital":
            return DigitalProduct(
                product_id, name, price, stock_quantity, supplier, download_size
            )
        else:
            raise ValueError(f"Unknown product type: {product_type}")
