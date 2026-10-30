import json
import os

from product import Product
from inventory import Inventory

INVENTORY_FILE = os.environ.get("INVENTORY_FILE", "inventory.json")


# ------------------------------------------------------------ file handling
def load_inventory(inventory):
    """Return True if loading succeeds or no file exists."""
    filename = os.path.basename(INVENTORY_FILE)

    try:
        with open(INVENTORY_FILE, "r") as f:
            records = json.load(f)

        if not isinstance(records, list):
            raise ValueError("Inventory data must be a list.")

        temporary_inventory = Inventory()

        for record in records:
            if not isinstance(record, dict):
                raise ValueError("Each product must be a dictionary.")

            product = Product.from_dict(record)

            if not isinstance(product.product_id, str):
                raise ValueError("Product ID must be text.")

            if not product.product_id.strip():
                raise ValueError("Product ID cannot be empty.")

            if not temporary_inventory.add_product(product):
                raise ValueError(
                    f"Duplicate product ID: {product.product_id}"
                )

    except FileNotFoundError:
        print(f"{filename} not found. Starting with an empty inventory.")
        return True

    except (OSError, ValueError, KeyError, TypeError) as error:
        print(f"Could not load {filename}: {error}")
        return False

    # This runs only after all records have passed the checks.
    for product in temporary_inventory.get_products():
        inventory.add_product(product)

    print("Inventory loaded successfully.")
    return True


def save_inventory(inventory):
    """Return True if the inventory is saved successfully."""
    records = [
        product.to_dict()
        for product in inventory.get_products()
    ]

    temporary_file = INVENTORY_FILE + ".tmp"

    try:
        with open(temporary_file, "w") as f:
            json.dump(records, f, indent=4)

        os.replace(temporary_file, INVENTORY_FILE)

    except OSError as error:
        print(f"Could not save inventory: {error}")
        return False

    print(
        f"Inventory saved successfully to "
        f"{os.path.basename(INVENTORY_FILE)}."
    )
    return True


# --------------------------------------------------------------- menu actions
def add_product(inventory):
    print("\nAdd New Product")
    product_id = input("Product ID: ").strip().upper()
    if not product_id:
        print("Product ID cannot be empty.")
        return
    if inventory.search_product(product_id):
        print("A product with that ID already exists.")
        return

    name = input("Product Name: ").strip()
    if not name:
        print("Product name cannot be empty.")
        return
    
    try:
        price = float(input("Price: "))
        stock = int(input("Stock Quantity: "))
    except ValueError:
        print("Invalid number entered. Product not added.")
        return

    try:
        product = Product(product_id, name, price, stock)
    except ValueError:
        print("Price and stock cannot be negative. Product not added.")
        return

    inventory.add_product(product)
    print("Product added successfully!")


def update_stock(inventory):
    print("\nUpdate Stock")
    product = inventory.search_product(input("Enter Product ID: ").strip())
    if product is None:
        print("Product not found.")
        return

    print("Product Found:")
    print(f"Name: {product.name}")
    print(f"Current Stock: {product.stock}")
    try:
        new_stock = int(input("New Stock Quantity: "))
    except ValueError:
        print("Invalid number entered. Stock not updated.")
        return

    try:
        product.update_stock(new_stock)
    except ValueError:
        print("Stock cannot be negative. Stock not updated.")
        return
    print("Stock updated successfully!")


def search_product(inventory):
    print("\nSearch Product")
    product = inventory.search_product(input("Enter Product ID: ").strip())
    if product is None:
        print("Product not found.")
        return
    product.display_information()


def show_menu():
    print("\n----------- MENU -----------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Save Inventory")
    print("6. Exit")
    print("----------------------------")


# ------------------------------------------------------------------- main
def main():
    print("=" * 40)
    print("INVENTORY MANAGEMENT SYSTEM")
    print("=" * 40)

    inventory = Inventory()

    if not load_inventory(inventory):
        print("Please fix the inventory file and restart the program.")
        return

    while True:
        show_menu()
        try:
            choice = input("Enter option: ").strip()
        except EOFError:
            choice = "6"

        if choice == "1":
            inventory.display_all()
        elif choice == "2":
            add_product(inventory)
        elif choice == "3":
            update_stock(inventory)
        elif choice == "4":
            search_product(inventory)
        elif choice == "5":
            print("Saving inventory...")
            save_inventory(inventory)
        elif choice == "6":
            print("Saving inventory before exit...")
            if save_inventory(inventory):
                print("Thank you for using Inventory Management System.")
                print("Program terminated.")
                break
            print("Exit cancelled because saving failed.")
        else:
            print("Invalid option. Please choose 1-6.")


if __name__ == "__main__":
    main()