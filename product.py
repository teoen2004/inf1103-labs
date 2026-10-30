class Product:
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