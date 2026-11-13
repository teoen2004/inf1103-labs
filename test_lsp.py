from supplier import Supplier
from product import Product, PhysicalProduct, DigitalProduct
from inventory import Inventory


def show_product_details(product: Product) -> None:
    """Works with ANY Product. No isinstance() checks, no subclass-specific code."""
    product.display_information()
    print(product.get_fulfilment_info())


supplier = Supplier("S001", "Acme Supplies", "sales@acme.com")
laptop = PhysicalProduct("P200", "Laptop", 1200.0, 10, supplier, 2.5)
ebook = DigitalProduct("D200", "Python eBook", 25.0, 100, supplier, 15.0)

# 6.2 (a) The same function accepts both subclasses unchanged.
print("=== show_product_details() with a PhysicalProduct ===")
show_product_details(laptop)
print("\n=== show_product_details() with a DigitalProduct ===")
show_product_details(ebook)

# 6.2 (b) Both types work with the Inventory's normal operations.
inventory = Inventory()
print("\n=== Inventory operations with both product types ===")
print("add laptop:", inventory.add_product(laptop))
print("add ebook: ", inventory.add_product(ebook))
print("find P200 is laptop:", inventory.find_product("P200") is laptop)
print("find D200 is ebook: ", inventory.find_product("D200") is ebook)
inventory.display_all_products()

# 6.3 Expectation set by Product.update_stock():
#     any quantity >= 0 is accepted and becomes the new stock;
#     a negative quantity raises ValueError. Both subclasses must keep this.
print("\n=== update_stock() keeps the same meaning for every Product ===")
for product in inventory.get_products():
    product.update_stock(5)
    print(f"{product.product_id}: update_stock(5) -> stock = {product.stock}")
    try:
        product.update_stock(-1)
        print(f"{product.product_id}: update_stock(-1) was accepted (LSP problem!)")
    except ValueError as error:
        print(f"{product.product_id}: update_stock(-1) -> ValueError: {error}")

print("\nremove ebook:", inventory.remove_product("D200") is ebook)
inventory.display_all()
