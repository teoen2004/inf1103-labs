from supplier import Supplier
from product import PhysicalProduct, DigitalProduct
from order import Order

supplier = Supplier("S001", "Acme Supplies", "sales@acme.com")
laptop = PhysicalProduct("P100", "Laptop", 1200.0, 10, supplier, 2.5)
mouse = PhysicalProduct("P101", "Mouse", 25.0, 50, supplier, 0.1)
ebook = DigitalProduct("D100", "Python eBook", 25.0, 100, supplier, 15.0)

# 1. Create an Order.
order1 = Order("O001")

# 2. Add products. The Order creates each OrderLine itself.
order1.add_order_line(laptop, 1)
order1.add_order_line(mouse, 2)
order1.add_order_line(ebook, 3)

# 3. Display each order line and the total.
print("\n=== Order 1 ===")
order1.display_order()

# 4. Add the SAME Product to a different Order.
order2 = Order("O002")
order2.add_order_line(laptop, 2)

print("\n=== Order 2 ===")
order2.display_order()

line_in_order1 = order1.get_order_lines()[0]
line_in_order2 = order2.get_order_lines()[0]

print("\n=== Same Product, different Orders ===")
print("Same OrderLine object?", line_in_order1 is line_in_order2)
print("Same Product object?  ", line_in_order1.product is line_in_order2.product)
print("id(OrderLine in O001):", id(line_in_order1))
print("id(OrderLine in O002):", id(line_in_order2))
print("id(laptop) in O001:   ", id(line_in_order1.product))
print("id(laptop) in O002:   ", id(line_in_order2.product))

# 5a. Remove an order line through the Order.
print("\n=== Order 1 after removing the eBook line ===")
print("Removed:", order1.remove_order_line("D100"))
order1.display_order()
print("Removing a line that is not there:", order1.remove_order_line("X999"))

# 5b. Outside code cannot add a line by changing the returned list.
order1.get_order_lines().clear()
print("\nLines still in Order 1 after clearing the COPY:", len(order1.get_order_lines()))

# 5c. Remove the whole Order: its lines go with it, the Products do not.
del line_in_order1, line_in_order2, order1
print("\n=== After 'del order1' ===")
print("Laptop still exists:", laptop)
print("Order 2 is unaffected:")
order2.display_order()

# 6. Invalid quantity is rejected by the OrderLine.
print("\n=== Invalid quantity ===")
try:
    order2.add_order_line(mouse, 0)
except ValueError as error:
    print("Rejected:", error)