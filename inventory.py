class Inventory:
    """Manages a COLLECTION of Product objects (SRP). No input(), no files, no menu."""

    def __init__(self):
        self.__products = []

    def add_product(self, product):
        """Add a Product. Returns False (and adds nothing) if the ID already exists."""
        if self.search_product(product.product_id) is not None:
            return False
        self.__products.append(product)
        return True

    def search_product(self, product_id):
        """Return the Product with this ID (case-insensitive), or None."""
        for product in self.__products:
            if product.product_id.lower() == product_id.lower():
                return product
        return None

    def display_all(self):
        print("\nCurrent Inventory")
        print("-" * 48)
        if not self.__products:
            print("Inventory is empty.")
        for product in self.__products:
            print(product)
        print("-" * 48)

    def get_products(self):
        """Return a copy of the product list (used by the file-saving code)."""
        return list(self.__products)