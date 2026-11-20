import unittest

from discount import (
    BulkDiscount,
    DiscountStrategy,
    NoDiscount,
    PercentageDiscount,
    StudentDiscount,
)
from order import Order
from product_factory import ProductFactory
from supplier import Supplier


class TestDiscountStrategy(unittest.TestCase):
    def setUp(self) -> None:
        self.supplier = Supplier("S001", "Acme Supplies", "sales@acme.com")
        self.item = ProductFactory.create(
            "physical", "P001", "Monitor", 125.0, 10, self.supplier, weight=3.0
        )

    def test_default_strategy_is_no_discount(self) -> None:
        order = Order("O001")
        order.add_order_line(self.item, 2)  # subtotal = 250.0
        self.assertIsInstance(order.discount, NoDiscount)
        self.assertAlmostEqual(order.calculate_total(), 250.0)

    def test_bulk_discount_and_swap_with_set_discount(self) -> None:
        order = Order("O002", BulkDiscount(200, 20))
        order.add_order_line(self.item, 2)  # subtotal = 250.0
        self.assertAlmostEqual(order.calculate_total(), 230.0)

        order.set_discount(PercentageDiscount(10))
        self.assertAlmostEqual(order.calculate_total(), 225.0)

    def test_bulk_discount_below_threshold_leaves_total_unchanged(self) -> None:
        order = Order("O003", BulkDiscount(200, 20))
        order.add_order_line(self.item, 1)  # subtotal = 125.0 < 200
        self.assertAlmostEqual(order.calculate_total(), 125.0)

    def test_student_discount_works_without_modifying_order(self) -> None:
        order = Order("O004", StudentDiscount())  # default 5%
        order.add_order_line(self.item, 2)  # subtotal = 250.0
        self.assertAlmostEqual(order.calculate_total(), 237.5)

    def test_custom_strategy_extension_ocp(self) -> None:
        class FlatTenDiscount(DiscountStrategy):
            def apply(self, total: float) -> float:
                return max(0.0, total - 10.0)

        order = Order("O005", FlatTenDiscount())
        order.add_order_line(self.item, 1)  # subtotal = 125.0
        self.assertAlmostEqual(order.calculate_total(), 115.0)

    def test_two_orders_can_share_same_strategy_association(self) -> None:
        shared_discount = PercentageDiscount(10)
        order1 = Order("O006", shared_discount)
        order2 = Order("O007", shared_discount)
        order1.add_order_line(self.item, 2)
        order2.add_order_line(self.item, 1)

        self.assertIs(order1.discount, order2.discount)
        self.assertAlmostEqual(order1.calculate_total(), 225.0)
        self.assertAlmostEqual(order2.calculate_total(), 112.5)


if __name__ == "__main__":
    unittest.main()
