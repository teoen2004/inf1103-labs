from supplier import Supplier
from product import PhysicalProduct, DigitalProduct

# 1. Create the Supplier on its own, before any Product exists.
supplier = Supplier("S001", "Acme Supplies", "sales@acme.com")

# 2. Pass the SAME Supplier object into two different products.
laptop = PhysicalProduct("P100", "Laptop", 1200.0, 10, supplier, 2.5)
ebook = DigitalProduct("D100", "Python eBook", 25.0, 100, supplier, 15.0)

# 3. Display the supplier information through each Product.
print("\n=== Supplier via laptop ===")
laptop.supplier.display_information()
print("\n=== Supplier via ebook ===")
ebook.supplier.display_information()

# 4. Separate objects that refer to each other.
print("\n=== Separate objects? ===")
print("Both products point to the same Supplier:", laptop.supplier is ebook.supplier)
print("Supplier is a different object from the laptop:", supplier is not laptop)
print("id(supplier):        ", id(supplier))
print("id(laptop.supplier): ", id(laptop.supplier))

# 5. Delete supplier
del supplier
print("\n=== After 'del supplier' ===")
print(laptop)
print(ebook)
laptop.supplier.display_information()