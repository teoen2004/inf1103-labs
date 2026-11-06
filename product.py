from abc import ABC, abstractmethod

class Product(ABC):
    """Represents and manages ONE product (SRP: one product, its data and its state)."""

    def __init__(self, product_id, name, price, stock):
        self.__product_id = product_id
        self.__name = name
        self.__price = None
        self.__stock = None
        # Go through the same checks used elsewhere so a Product can never start invalid.
        self.__set_price(price)
        self.update_stock(stock)

    # ----------------------------------------------------- read-only access
    @property
    def product_id(self):
        return self.__product_id

    @property
    def name(self):
        return self.__name

    @property
    def price(self):
        return self.__price

    @property
    def stock(self):
        return self.__stock

    # ------------------------------------------------------ managing state
    def __set_price(self, price):
        if price < 0:
            raise ValueError("Price cannot be negative.")
        self.__price = price

    def update_stock(self, quantity):
        """Set the stock level. The Product decides what is a valid value."""
        if quantity < 0:
            raise ValueError("Stock cannot be negative.")
        self.__stock = quantity

    # ------------------------------------------------------------- display
    def display_information(self):
        print("Product Found")
        print("-" * 48)
        print(f"ID: {self.__product_id}")
        print(f"Name: {self.__name}")
        print(f"Price: ${self.__price:.2f}")
        print(f"Stock: {self.__stock}")
        print("-" * 48)

    def __str__(self):
        """One-line summary, used by Inventory.display_all()."""
        return (f"ID: {self.__product_id} | Name: {self.__name} | "
                f"Price: ${self.__price:.2f} | Stock: {self.__stock}")

    # ------------------------------------------- conversion for JSON storage
    def to_dict(self):
        """Describe this product as a plain dict (the file code decides how to store it)."""
        return {"id": self.__product_id, "name": self.__name,
                "price": self.__price, "stock": self.__stock}

    @classmethod
    def from_dict(cls, data):
        return cls(data["id"], data["name"], data["price"], data["stock"])

    @abstractmethod
    def get_fulfilment_info(self):
        """Return a string describing how this product is fulfilled (e.g., shipped, downloaded)."""
        pass


class CanBeShipped(ABC):
    @abstractmethod
    def calculate_shipping_cost(self):
        """Return the shipping cost for this product."""
        pass


class PhysicalProduct(Product, CanBeShipped):
    def __init__(self, product_id, name, price, stock, weight):
        super().__init__(product_id, name, price, stock)

        if weight < 0:
            raise ValueError("Weight cannot be negative.")
        
        self.__weight = weight

        super().display_information()
        print(f"Weight: {self.__weight} kg")

    def get_fulfilment_info(self):
        return "This product requires physical shipping."

    def calculate_shipping_cost(self):
        return self.__weight * 2

    def to_dict(self):
        data = super().to_dict()
        data["type"] = "physical"
        data["weight"] = self.__weight
        return data

    @property
    def weight(self):
        return self.__weight



class DigitalProduct(Product):
    def __init__(self, product_id, name, price, stock, download_size):
        super().__init__(product_id, name, price, stock)
        self.__download_size = download_size

        super().display_information()
        print(f"File Size: {self.__download_size} MB")

    def get_fulfilment_info(self):
        return "This product is delivered digitally."

    def to_dict(self):
        data = super().to_dict()
        data["type"] = "digital"
        data["download_size"] = self.__download_size
        return data
    
    @property
    def download_size(self):
        return self.__download_size
