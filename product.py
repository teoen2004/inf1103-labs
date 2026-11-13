from abc import ABC, abstractmethod

from supplier import Supplier


class Product(ABC):
    """Represents and manages ONE product (SRP: one product, its data and its state)."""

    def __init__(self, product_id: str, name: str, price: float, stock: int,
                 supplier: Supplier) -> None:
        self.__product_id: str = product_id
        self.__name: str = name
        self.__price: float | None = None
        self.__stock: int | None = None
        self.__supplier: Supplier = supplier   # a reference, not a copy
        # Go through the same checks used elsewhere so a Product can never start invalid.
        self.__set_price(price)
        self.update_stock(stock)

    # ----------------------------------------------------- read-only access
    @property
    def product_id(self) -> str:
        return self.__product_id

    @property
    def name(self) -> str:
        return self.__name

    @property
    def price(self) -> float:
        return self.__price

    @property
    def stock(self) -> int:
        return self.__stock

    @property
    def supplier(self) -> Supplier:
        return self.__supplier

    # ------------------------------------------------------ managing state
    def __set_price(self, price: float) -> None:
        if price < 0:
            raise ValueError("Price cannot be negative.")
        self.__price = price

    def update_stock(self, quantity: int) -> None:
        """Set the stock level. The Product decides what is a valid value."""
        if quantity < 0:
            raise ValueError("Stock cannot be negative.")
        self.__stock = quantity

    # ------------------------------------------------------------- display
    def display_information(self) -> None:
        print("Product Found")
        print("-" * 48)
        print(f"ID: {self.__product_id}")
        print(f"Name: {self.__name}")
        print(f"Price: ${self.__price:.2f}")
        print(f"Stock: {self.__stock}")
        print(f"Supplier: {self.__supplier.name} ({self.__supplier.contact_email})")
        print("-" * 48)

    def __str__(self) -> str:
        """One-line summary, used by Inventory.display_all()."""
        return (f"ID: {self.__product_id} | Name: {self.__name} | "
                f"Price: ${self.__price:.2f} | Stock: {self.__stock} | "
                f"Supplier: {self.__supplier.name}")

    # ------------------------------------------- conversion for JSON storage
    def to_dict(self) -> dict:
        """Describe this product as a plain dict (the file code decides how to store it)."""
        return {"id": self.__product_id, "name": self.__name,
                "price": self.__price, "stock": self.__stock,
                "supplier": self.__supplier.to_dict()}

    @abstractmethod
    def get_fulfilment_info(self) -> str:
        """Return a string describing how this product is fulfilled (e.g., shipped, downloaded)."""
        pass


class CanBeShipped(ABC):
    @abstractmethod
    def calculate_shipping_cost(self) -> float:
        """Return the shipping cost for this product."""
        pass


class PhysicalProduct(Product, CanBeShipped):
    def __init__(self, product_id: str, name: str, price: float, stock: int,
                 supplier: Supplier, weight: float) -> None:
        super().__init__(product_id, name, price, stock, supplier)

        if weight < 0:
            raise ValueError("Weight cannot be negative.")

        self.__weight: float = weight

        super().display_information()
        print(f"Weight: {self.__weight} kg")

    def get_fulfilment_info(self) -> str:
        return "This product requires physical shipping."

    def calculate_shipping_cost(self) -> float:
        return self.__weight * 2

    def to_dict(self) -> dict:
        data = super().to_dict()
        data["type"] = "physical"
        data["weight"] = self.__weight
        return data

    @property
    def weight(self) -> float:
        return self.__weight



class DigitalProduct(Product):
    def __init__(self, product_id: str, name: str, price: float, stock: int,
                 supplier: Supplier, download_size: float) -> None:
        super().__init__(product_id, name, price, stock, supplier)
        self.__download_size: float = download_size

        super().display_information()
        print(f"File Size: {self.__download_size} MB")

    def get_fulfilment_info(self) -> str:
        return "This product is delivered digitally."

    def to_dict(self) -> dict:
        data = super().to_dict()
        data["type"] = "digital"
        data["download_size"] = self.__download_size
        return data

    @property
    def download_size(self) -> float:
        return self.__download_size
