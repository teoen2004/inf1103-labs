import json
import os

INVENTORY_FILE = os.environ.get("INVENTORY_FILE", "inventory.json")

inventory = [
    {"id": "P001", "name": "Laptop",   "price": 1200.00, "stock": 15},
    {"id": "P002", "name": "Mouse",    "price": 25.50,   "stock": 40},
    {"id": "P003", "name": "Keyboard", "price": 45.00,   "stock": 25},
]

# The inventory is a list of dictionaries, one dictionary per product.
inventory = []

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

def display_all():
    print("\nCurrent Inventory")
    print("-" * 48)
    if not inventory:
        print("Inventory is empty.")
    for p in inventory:
        print(f"ID: {p['id']} | Name: {p['name']} | Price: ${p['price']:.2f} | Stock: {p['stock']}")
    print("-" * 48)

load_inventory()
display_all()