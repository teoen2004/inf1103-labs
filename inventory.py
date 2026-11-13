from product import Product


class Inventory:
    """Manages a COLLECTION of Product objects (SRP). No input(), no files, no menu.

    Aggregation with Product: the Inventory holds references to Products that were
    created elsewhere. Adding or removing a product never creates or destroys it.
    """

    def __init__(self) -> None:
        self.__products: list[Product] = []

    def add_product(self, product: Product) -> bool:
        """Add an existing Product. Returns False (and adds nothing) if the ID already exists."""
        if self.find_product(product.product_id) is not None:
            return False
        self.__products.append(product)
        return True

    def remove_product(self, product_id: str) -> Product | None:
        """Remove the matching Product reference from this inventory.

        Returns the removed Product so it can be reused (e.g. added to another
        inventory), or None if no product has this ID. The Product itself is
        not destroyed, only this inventory's reference to it is removed.
        """
        product = self.find_product(product_id)
        if product is not None:
            self.__products.remove(product)
        return product

    def find_product(self, product_id: str) -> Product | None:
        """Return the Product with this ID (case-insensitive), or None."""
        for product in self.__products:
            if product.product_id.lower() == product_id.lower():
                return product
        return None

    def display_all(self) -> None:
        print("\nCurrent Inventory")
        print("-" * 48)
        if not self.__products:
            print("Inventory is empty.")
        for product in self.__products:
            print(product)
        print("-" * 48)

    def display_all_products(self) -> None:
        """Ask every Product to display itself. Inventory never checks the subclass:
        each object runs its own display_information()"""
        if not self.__products:
            print("Inventory is empty.")
        for product in self.__products:
            product.display_information()

    def get_products(self) -> list[Product]:
        """Return a copy of the product list (used by the file-saving code)."""
        return list(self.__products)