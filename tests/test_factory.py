import unittest

from product import DigitalProduct, PhysicalProduct, Product
from product_factory import ProductFactory
from supplier import Supplier


class TestProductFactory(unittest.TestCase):
    def setUp(self) -> None:
        self.supplier = Supplier("S001", "Acme Supplies", "sales@acme.com")

    def test_create_physical_product(self) -> None:
        product = ProductFactory.create(
            "physical", "P001", "Desk Lamp", 25.00, 10, self.supplier, weight=1.5
        )
        self.assertIsInstance(product, Product)
        self.assertIsInstance(product, PhysicalProduct)
        self.assertEqual(product.product_id, "P001")
        self.assertEqual(product.weight, 1.5)

    def test_create_digital_product(self) -> None:
        product = ProductFactory.create(
            "digital", "D001", "Photo Editor", 49.90, 100, self.supplier, download_size=500.0
        )
        self.assertIsInstance(product, Product)
        self.assertIsInstance(product, DigitalProduct)
        self.assertEqual(product.product_id, "D001")
        self.assertEqual(product.download_size, 500.0)

    def test_unknown_product_type_raises_value_error(self) -> None:
        with self.assertRaises(ValueError) as context:
            ProductFactory.create(
                "service", "S001", "Installation", 30.00, 5, self.supplier
            )
        self.assertIn("Unknown product type: service", str(context.exception))


if __name__ == "__main__":
    unittest.main()
