def get_valid_input():
    """Handles prompt, validates input, returns valid int, None (invalid), or 'quit'."""
    user_input = input("Enter delivery stock quantity (or 'quit' to exit): ").strip()

    if user_input.lower() == 'quit':
        return 'quit'

    try:
        val = int(user_input)
        if val < 0:
            print("Error: Quantity cannot be negative.")
            return None
        return val
    except ValueError:
        print("Error: Please enter a valid whole number or 'quit'.")
        return None


def process_delivery(current_total, new_value):
    """Calculates and returns the new total."""
    return current_total + new_value


def calculate_tax(amount):
    """Calculates and returns 10% tax for a specific delivery amount."""
    return amount * 0.10


def generate_report(total_units, failed_attempts, total_deliveries, max_capacity, total_tax_collected):
    """Prints the final summary report."""
    print("\n==================================")
    print("      INVENTORY AUDIT REPORT      ")
    print("==================================")
    print(f"Total Deliveries Processed : {total_deliveries}")
    print(f"Total Inventory Units     : {total_units} / {max_capacity}")
    print(f"Failed/Rejected Entries   : {failed_attempts}")
    print(f"Total Tax Collected       : ${total_tax_collected:.2f}")
    print("==================================")


def main():
    # Local variables & configuration inside main scope
    max_capacity = 500
    total_units = 0
    total_deliveries = 0
    failed_attempts = 0
    total_tax_collected = 0

    while True:
        entry = get_valid_input()

        if entry == 'quit':
            break

        if entry is None:
            failed_attempts += 1
        elif total_units + entry > max_capacity:
            # Rejects entry if it exceeds local max_capacity
            print(f"Error: Delivery of {entry} units would exceed max capacity ({max_capacity}). Current total: {total_units}.")
            failed_attempts += 1
        else:
            total_units = process_delivery(total_units, entry)
            tax_amount = calculate_tax(entry)
            total_deliveries += 1
            total_tax_collected += tax_amount
            print(f"-> Logged delivery: {entry} units | Tax for delivery: ${tax_amount:.2f}")

    # Pass max_capacity into report generator
    generate_report(total_units, failed_attempts, total_deliveries, max_capacity, total_tax_collected)


if __name__ == "__main__":
    main()