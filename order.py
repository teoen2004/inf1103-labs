from product import Product


class OrderLine:

    def __init__(self, product: Product, quantity: int) -> None:
        if quantity <= 0:
            raise ValueError("Quantity must be at least 1.")
        self.__product: Product = product
        self.__quantity: int = quantity

    # ----------------------------------------------------- read-only access
    @property
    def product(self) -> Product:
        return self.__product

    @property
    def quantity(self) -> int:
        return self.__quantity

    # ---------------------------------------------------------- behaviour
    def calculate_subtotal(self) -> float:
        return self.__product.price * self.__quantity

    def __str__(self) -> str:
        return (f"{self.__product.product_id} | {self.__product.name} | "
                f"Qty: {self.__quantity} | Unit: ${self.__product.price:.2f} | "
                f"Subtotal: ${self.calculate_subtotal():.2f}")


class Order:
    """Represents ONE customer order and OWNS its OrderLine objects (composition).

    The Order creates its own OrderLines in add_order_line(). OrderLines are
    never passed in from outside and never moved to another Order.
    """

    def __init__(self, order_id: str) -> None:
        self.__order_id: str = order_id
        self.__order_lines: list[OrderLine] = []

    # ----------------------------------------------------- read-only access
    @property
    def order_id(self) -> str:
        return self.__order_id

    def get_order_lines(self) -> list[OrderLine]:
        """Return a copy of the list, so outside code cannot add lines directly."""
        return list(self.__order_lines)

    # ------------------------------------------------ managing order lines
    def add_order_line(self, product: Product, quantity: int) -> None:
        """Create a NEW OrderLine inside this Order (the Order is responsible for it)."""
        order_line = OrderLine(product, quantity)
        self.__order_lines.append(order_line)

    def remove_order_line(self, product_id: str) -> bool:
        """Remove the line for this product. Returns False if no line matches.

        Returns True/False rather than the OrderLine itself, so a removed line
        cannot be handed to another Order.
        """
        for order_line in self.__order_lines:
            if order_line.product.product_id.lower() == product_id.lower():
                self.__order_lines.remove(order_line)
                return True
        return False

    # ---------------------------------------------------------- behaviour
    def calculate_total(self) -> float:
        """Ask each OrderLine for its subtotal and add them up."""
        return sum((line.calculate_subtotal() for line in self.__order_lines), 0.0)

    def display_order(self) -> None:
        print(f"\nOrder {self.__order_id}")
        print("-" * 72)
        if not self.__order_lines:
            print("Order has no lines.")
        for order_line in self.__order_lines:
            print(order_line)
        print("-" * 72)
        print(f"Total: ${self.calculate_total():.2f}")