from supplier import Supplier
from product_factory import ProductFactory
from inventory import Inventory

# Section 7: Polymorphism through the common Product type.
# Rules: ONE loop for every product, no isinstance(), no separate
# loops for physical and digital products.

supplier = Supplier("S001", "Acme Supplies", "sales@acme.com")

inventory = Inventory()
inventory.add_product(ProductFactory.create("physical", "P300", "Office Chair", 150.0, 20, supplier, weight=12.0))
inventory.add_product(ProductFactory.create("digital", "D300", "Antivirus Licence", 49.9, 500, supplier, download_size=250.0))
inventory.add_product(ProductFactory.create("physical", "P301", "USB Keyboard", 35.0, 40, supplier, weight=0.8))
inventory.add_product(ProductFactory.create("digital", "D301", "Design Course", 89.0, 1000, supplier, download_size=4096.0))

print("=== One loop, every Product, no type checks ===\n")
for product in inventory.get_products():
    # The SAME two calls for every object. Python picks the subclass
    # implementation based on the object's actual class at runtime.
    product.display_information()
    print(f"Fulfilment: {product.get_fulfilment_info()}")
    print(f"(actual class: {type(product).__name__})\n")
