import csv
import json
import os

from inventory import Inventory
from product_factory import ProductFactory
from supplier import Supplier

INVENTORY_FILE = os.environ.get("INVENTORY_FILE", "inventory.json")


# ----------------------------------------------------------- input helpers
def get_positive_float(prompt: str) -> float:
    """Ask the user for a positive floating-point number until a valid one is entered."""
    while True:
        try:
            value = float(input(prompt))
            if value <= 0:
                print("Please enter a number greater than zero.")
                continue
            return value
        except ValueError:
            print("Please enter a valid number, e.g. 12.50")


def get_non_negative_int(prompt: str) -> int:
    """Ask the user for a non-negative integer until a valid one is entered."""
    while True:
        try:
            value = int(input(prompt))
            if value < 0:
                print("Please enter a whole number of 0 or more.")
                continue
            return value
        except ValueError:
            print("Please enter a valid whole number, e.g. 10")


def get_non_negative_float(prompt: str) -> float:
    """Ask the user for a non-negative floating-point number until a valid one is entered."""
    while True:
        try:
            value = float(input(prompt))
            if value < 0:
                print("Please enter a number of 0 or more.")
                continue
            return value
        except ValueError:
            print("Please enter a valid number, e.g. 2.5")


# ------------------------------------------------------------ file handling
def load_products(path: str, inventory: Inventory, supplier: Supplier) -> None:
    """Load products from a CSV file using ProductFactory and add valid rows to inventory."""
    loaded = 0
    try:
        file = open(path, newline="", encoding="utf-8")
    except FileNotFoundError:
        print(f"Products file not found: {path}")
    else:
        with file:
            reader = csv.reader(file)
            next(reader, None)  # skip header row
            for row_num, row in enumerate(reader, start=2):
                try:
                    if len(row) != 5:
                        raise ValueError(f"Expected 5 columns, got {len(row)}")
                    product_type, product_id, name, price_str, stock_str = row
                    price = float(price_str)
                    stock_quantity = int(stock_str)
                    product = ProductFactory.create(
                        product_type,
                        product_id,
                        name,
                        price,
                        stock_quantity,
                        supplier,
                    )
                    if inventory.add_product(product):
                        loaded += 1
                    else:
                        print(f"Row {row_num} skipped: Duplicate product ID '{product_id}'.")
                except ValueError as error:
                    print(f"Row {row_num} skipped: {error}")
        print(f"{loaded} products loaded.")
    finally:
        print("Load attempt finished.")
def build_supplier(data: dict[str, str] | None, suppliers: dict[str, Supplier]) -> Supplier:
    """Return ONE shared Supplier object per supplier ID while loading."""
    if data is None:  # records saved before Lab 8 have no supplier
        data = {"id": "UNKNOWN", "name": "Unknown Supplier", "email": "N/A"}

    if data["id"] not in suppliers:
        suppliers[data["id"]] = Supplier(data["id"], data["name"], data["email"])
    return suppliers[data["id"]]


def load_inventory(inventory: Inventory) -> bool:
    """Return True if loading succeeds or no file exists."""
    filename = os.path.basename(INVENTORY_FILE)

    try:
        with open(INVENTORY_FILE, "r") as f:
            records = json.load(f)

        if not isinstance(records, list):
            raise ValueError("Inventory data must be a list.")

        temporary_inventory = Inventory()
        suppliers: dict[str, Supplier] = {}

        for record in records:
            if not isinstance(record, dict):
                raise ValueError("Each product must be a dictionary.")

            supplier = build_supplier(record.get("supplier"), suppliers)
            product_type = record.get("type")
            if not isinstance(product_type, str):
                raise ValueError("Unknown product type.")

            product = ProductFactory.create(
                product_type,
                record["id"],
                record["name"],
                record["price"],
                record["stock"],
                supplier,
                weight=record.get("weight", 0.0),
                download_size=record.get("download_size", 0.0),
            )

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


def save_inventory(inventory: Inventory) -> bool:
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
def find_supplier(inventory: Inventory, supplier_id: str) -> Supplier | None:
    """Reuse a Supplier that is already linked to a product in the inventory."""
    for product in inventory.get_products():
        if product.supplier.supplier_id.lower() == supplier_id.lower():
            return product.supplier
    return None


def add_product(inventory: Inventory) -> None:
    print("\nAdd New Product")
    print("1. Physical Product")
    print("2. Digital Product")

    product_type = input("Select product type (1 or 2): ").strip()
    
    if product_type not in ("1", "2"):
        print("Invalid product type.")
        return

    product_id = input("Product ID: ").strip().upper()
    
    if not product_id:
        print("Product ID cannot be empty.")
        return
    
    if inventory.find_product(product_id):
        print("A product with that ID already exists.")
        return

    name = input("Product Name: ").strip()

    if not name:
        print("Product name cannot be empty.")
        return

    supplier_id = input("Supplier ID: ").strip().upper()
    supplier = find_supplier(inventory, supplier_id)

    if supplier is None:
        supplier_name = input("Supplier Name: ").strip()
        supplier_email = input("Supplier Email: ").strip()
        supplier = Supplier(supplier_id, supplier_name, supplier_email)
    else:
        print(f"Using existing supplier: {supplier.name}")
    
    price = get_positive_float("Price: ")
    stock = get_non_negative_int("Stock Quantity: ")

    try:
        if product_type == "1":
            weight = get_non_negative_float("Weight (kg): ")
            product = ProductFactory.create(
                "physical", product_id, name, price, stock, supplier, weight=weight
            )
        else:
            download_size = get_non_negative_float("Download Size (MB): ")
            product = ProductFactory.create(
                "digital",
                product_id,
                name,
                price,
                stock,
                supplier,
                download_size=download_size,
            )
    except ValueError as error:
        print(f"Invalid product information. {error}")
        return

    inventory.add_product(product)
    print("Product added successfully!")


def update_stock(inventory: Inventory) -> None:
    print("\nUpdate Stock")
    product = inventory.find_product(input("Enter Product ID: ").strip())
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


def search_product(inventory: Inventory) -> None:
    print("\nSearch Product")
    product = inventory.find_product(input("Enter Product ID: ").strip())
    if product is None:
        print("Product not found.")
        return
    product.display_information()


def load_products_from_csv(inventory: Inventory) -> None:
    print("\nLoad Products from CSV")
    path = input("CSV file path (default products.csv): ").strip() or "products.csv"
    supplier_id = input("Supplier ID (default S001): ").strip().upper() or "S001"
    supplier = find_supplier(inventory, supplier_id)
    if supplier is None:
        supplier = Supplier(supplier_id, "Default Supplier", "supplier@example.com")
    load_products(path, inventory, supplier)


def show_menu() -> None:
    print("\n----------- MENU -----------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Save Inventory")
    print("6. Load Products from CSV")
    print("7. Exit")
    print("----------------------------")


# ------------------------------------------------------------------- main
def main() -> None:
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
            choice = "7"

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
            load_products_from_csv(inventory)
        elif choice == "7":
            print("Saving inventory before exit...")
            if save_inventory(inventory):
                print("Thank you for using Inventory Management System.")
                print("Program terminated.")
                break
            print("Exit cancelled because saving failed.")
        else:
            print("Invalid option. Please choose 1-7.")


if __name__ == "__main__":
    main()