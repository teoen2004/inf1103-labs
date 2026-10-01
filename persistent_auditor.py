INVENTORY_FILE = "inventory.txt"

def load_inventory():
    orders = []
    try:
        with open(INVENTORY_FILE, "r") as file:
            for line in file:
                line = line.strip()
                if line:
                    orders.append(line)
    except FileNotFoundError:
        pass
    return orders

def save_inventory(orders):
    with open(INVENTORY_FILE, "w") as file:
        for order in orders:
            file.write(f"{order}\n")

def display_orders(orders):
    print("\nCurrent Orders:")
    if not orders:
        print("No orders found.")
    else:
        for order in orders:
            print(order)

def main():
    orders = load_inventory()
    display_orders(orders)
    print()

    next_id = 1001 + len(orders)  # Start IDs from 1001 and increment for each order

    while True:
        product_name = input("Enter product name (or type 'quit' to finish): ").strip().lower()
        if product_name == 'quit':
            break

        quantity_input = input("Enter quantity for the product: ").strip()
        if quantity_input.lower() == 'quit':
            break

        try:
            quantity = int(quantity_input)
            if quantity <= 0:
                print("\nQuantity cannot be negative. Please enter a valid quantity.")
                continue
            if quantity > 500:
                print("\nQuantity cannot exceed 500. Please enter a valid quantity.")
                continue
        except ValueError:
            print("\nPlease enter a valid number for quantity.")
            continue

        new_order = f"Order ID: {next_id}, Product: {product_name}, Quantity: {quantity}"
        orders.append(new_order)
        next_id += 1

        print(f"New Order Added:")
        print(new_order)

        save_inventory(orders)
        print("Order successfully saved to orders.txt\n")

if __name__ == "__main__":
    main()

