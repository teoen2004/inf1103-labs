import io
import os
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

from inventory import Inventory
from inventory_manager import get_positive_float, load_products
from supplier import Supplier


class TestErrorHandling(unittest.TestCase):
    def setUp(self) -> None:
        self.supplier = Supplier("S001", "Acme Supplies", "sales@acme.com")
        self.project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.csv_path = os.path.join(self.project_root, "products.csv")

    def test_get_positive_float_retries_until_valid(self) -> None:
        buffer = io.StringIO()
        with patch("builtins.input", side_effect=["abc", "-5", "12.50"]):
            with redirect_stdout(buffer):
                result = get_positive_float("Enter price: ")

        self.assertAlmostEqual(result, 12.50)
        lines = [line.strip() for line in buffer.getvalue().splitlines()]
        self.assertEqual(
            lines,
            [
                "Please enter a valid number, e.g. 12.50",
                "Please enter a number greater than zero.",
            ],
        )

    def test_load_products_skips_bad_rows_and_loads_valid_rows(self) -> None:
        inventory = Inventory()
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            load_products(self.csv_path, inventory, self.supplier)

        output = buffer.getvalue()
        products = inventory.get_products()
        self.assertEqual(len(products), 3)
        self.assertEqual([p.product_id for p in products], ["P001", "D001", "P003"])
        self.assertIn("Unknown product type: service", output)
        self.assertIn("could not convert string to float: 'abc'", output)
        self.assertIn("3 products loaded.", output)
        self.assertTrue(output.strip().endswith("Load attempt finished."))

    def test_load_products_missing_file_handled_gracefully(self) -> None:
        inventory = Inventory()
        missing_path = os.path.join(self.project_root, "missing_products.csv")
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            load_products(missing_path, inventory, self.supplier)

        lines = [line.strip() for line in buffer.getvalue().splitlines()]
        self.assertEqual(len(inventory.get_products()), 0)
        self.assertEqual(
            lines,
            [
                f"Products file not found: {missing_path}",
                "Load attempt finished.",
            ],
        )


if __name__ == "__main__":
    unittest.main()
