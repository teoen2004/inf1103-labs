import json
import os

INVENTORY_FILE = os.environ.get("INVENTORY_FILE", "inventory.json")

# The inventory is a list of dictionaries, one dictionary per product.
inventory = []

# ---------------------------------------------------------------- persistence
def load_inventory():
    """Load inventory.json if it exists, otherwise start empty."""
    global inventory
    if os.path.exists(INVENTORY_FILE):
        print(f"{os.path.basename(INVENTORY_FILE)} found.")
        try:
            with open(INVENTORY_FILE, "r") as f:
                inventory = json.load(f)
            print("Inventory loaded successfully.")
        except (json.JSONDecodeError, OSError):
            print("Could not read the file. Starting with an empty inventory.")
            inventory = []
    else:
        print(f"{os.path.basename(INVENTORY_FILE)} not found. Starting with an empty inventory.")
        inventory = []

def save_inventory():
    """Write the current inventory list to inventory.json."""
    with open(INVENTORY_FILE, "w") as f:
        json.dump(inventory, f, indent=4)
    print(f"Inventory saved successfully to {os.path.basename(INVENTORY_FILE)}.")

# ------------------------------------------------------------------- CRUD
def find_product(product_id):
    """Return the product dictionary with this ID, or None."""
    for product in inventory:
        if product["id"].lower() == product_id.lower():
            return product
    return None


def add_product():
    print("\nAdd New Product")
    product_id = input("Product ID: ").strip().upper()
    if not product_id:
        print("Product ID cannot be empty.")
        return
    if find_product(product_id):
        print("A product with that ID already exists.")
        return

    name = input("Product Name: ").strip()
    try:
        price = float(input("Price: "))
        stock = int(input("Stock Quantity: "))
    except ValueError:
        print("Invalid number entered. Product not added.")
        return
    if price < 0 or stock < 0:
        print("Price and stock cannot be negative. Product not added.")
        return

    inventory.append({"id": product_id, "name": name, "price": price, "stock": stock})
    print("Product added successfully!")


def update_stock():
    print("\nUpdate Stock")
    product = find_product(input("Enter Product ID: ").strip())
    if product is None:
        print("Product not found.")
        return

    print("Product Found:")
    print(f"Name: {product['name']}")
    print(f"Current Stock: {product['stock']}")
    try:
        new_stock = int(input("New Stock Quantity: "))
    except ValueError:
        print("Invalid number entered. Stock not updated.")
        return
    if new_stock < 0:
        print("Stock cannot be negative. Stock not updated.")
        return

    product["stock"] = new_stock
    print("Stock updated successfully!")


def search_product():
    print("\nSearch Product")
    product = find_product(input("Enter Product ID: ").strip())
    if product is None:
        print("Product not found.")
        return

    print("Product Found")
    print("-" * 48)
    print(f"ID: {product['id']}")
    print(f"Name: {product['name']}")
    print(f"Price: ${product['price']:.2f}")
    print(f"Stock: {product['stock']}")
    print("-" * 48)


def display_all():
    print("\nCurrent Inventory")
    print("-" * 48)
    if not inventory:
        print("Inventory is empty.")
    for p in inventory:
        print(f"ID: {p['id']} | Name: {p['name']} | Price: ${p['price']:.2f} | Stock: {p['stock']}")
    print("-" * 48)


# ------------------------------------------------------------------- menu
def show_menu():
    print("\n----------- MENU -----------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Save Inventory")
    print("6. Exit")
    print("----------------------------")


def main():
    print("=" * 40)
    print("INVENTORY MANAGEMENT SYSTEM")
    print("=" * 40)
    load_inventory()

    while True:
        show_menu()
        try:
            choice = input("Enter option: ").strip()
        except EOFError:           # input stream closed (e.g. piped input ended)
            choice = "6"

        if choice == "1":
            display_all()
        elif choice == "2":
            add_product()
        elif choice == "3":
            update_stock()
        elif choice == "4":
            search_product()
        elif choice == "5":
            print("Saving inventory...")
            save_inventory()
        elif choice == "6":
            print("Saving inventory before exit...")
            save_inventory()
            print("Thank you for using Inventory Management System.")
            print("Program terminated.")
            break
        else:
            print("Invalid option. Please choose 1-6.")


if __name__ == "__main__":
    main()