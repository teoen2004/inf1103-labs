import unittest

from order import Order, OrderLine
from product_factory import ProductFactory
from supplier import Supplier


class TestValidation(unittest.TestCase):
    def setUp(self) -> None:
        self.supplier = Supplier("S001", "Acme Supplies", "sales@acme.com")
        self.valid_product = ProductFactory.create(
            "physical", "P001", "Desk Lamp", 25.00, 10, self.supplier
        )

    def test_product_price_must_be_greater_than_zero(self) -> None:
        for invalid_price in (0, -10.5):
            with self.assertRaises(ValueError):
                ProductFactory.create(
                    "physical", "P002", "Bad Price", invalid_price, 5, self.supplier
                )
            with self.assertRaises(ValueError):
                ProductFactory.create(
                    "digital", "D002", "Bad Digital Price", invalid_price, 5, self.supplier
                )

    def test_product_stock_cannot_be_negative(self) -> None:
        with self.assertRaises(ValueError):
            ProductFactory.create(
                "physical", "P003", "Negative Stock", 15.0, -1, self.supplier
            )
        with self.assertRaises(ValueError):
            ProductFactory.create(
                "digital", "D003", "Negative Digital Stock", 15.0, -5, self.supplier
            )

    def test_product_stock_zero_is_allowed_for_both_subclasses(self) -> None:
        phys = ProductFactory.create("physical", "P004", "Zero Phys", 10.0, 0, self.supplier)
        dig = ProductFactory.create("digital", "D004", "Zero Dig", 10.0, 0, self.supplier)
        self.assertEqual(phys.stock, 0)
        self.assertEqual(dig.stock, 0)

    def test_update_stock_rejects_negative_for_digital_and_physical_lsp(self) -> None:
        digital = ProductFactory.create("digital", "D005", "App", 20.0, 5, self.supplier)
        for product in (self.valid_product, digital):
            with self.assertRaises(ValueError):
                product.update_stock(-1)

    def test_order_line_quantity_must_be_greater_than_zero(self) -> None:
        for invalid_qty in (0, -3):
            with self.assertRaises(ValueError):
                OrderLine(self.valid_product, invalid_qty)

        order = Order("O100")
        with self.assertRaises(ValueError):
            order.add_order_line(self.valid_product, 0)


if __name__ == "__main__":
    unittest.main()
