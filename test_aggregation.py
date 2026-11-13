from supplier import Supplier
from product import PhysicalProduct, DigitalProduct
from inventory import Inventory

supplier = Supplier("S001", "Acme Supplies", "sales@acme.com")

# 1. Create a Product BEFORE any Inventory exists.
laptop = PhysicalProduct("P100", "Laptop", 1200.0, 10, supplier, 2.5)

inventory_a = Inventory()
inventory_b = Inventory()

# 2. Add the Product to Inventory A.
inventory_a.add_product(laptop)
print("\n=== Inventory A after adding the laptop ===")
inventory_a.display_all()

# 3. Remove it from Inventory A and check the Product can still be used.
removed = inventory_a.remove_product("P100")
print("\n=== Inventory A after removing the laptop ===")
inventory_a.display_all()
print("Removed object is the same laptop:", removed is laptop)
laptop.update_stock(8)
print("Laptop still works:", laptop)

# 4. Add the SAME Product object to Inventory B.
inventory_b.add_product(laptop)
print("\n=== Inventory B after adding the laptop ===")
inventory_b.display_all()
print("Inventory B holds the same laptop object:",
      inventory_b.find_product("P100") is laptop)

# 5. Empty Inventory B and confirm the products still exist.
ebook = DigitalProduct("D100", "Python eBook", 25.0, 100, supplier, 15.0)
inventory_b.add_product(ebook)

for product in inventory_b.get_products():
    inventory_b.remove_product(product.product_id)

print("\n=== Inventory B after emptying it ===")
inventory_b.display_all()
print("Laptop still exists:", laptop)
print("eBook still exists: ", ebook)

# 6. Edge cases: IDs that are not in the inventory.
print("\n=== Missing IDs ===")
print("remove_product('X999'):", inventory_a.remove_product("X999"))
print("find_product('X999'):  ", inventory_a.find_product("X999"))