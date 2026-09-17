inventory = 0
failed_entries = 0

while True:
    stock = input("Enter the number of items in stock (or type 'exit' to finish): ")

    # Check if the user wants to quit
    if stock.lower() == 'exit':
        print("\nTotal Units Processed:", inventory)
        print("Failed Entries:", failed_entries)
        break

    try:
        stock = int(stock) #check if the input is a valid integer

        if stock < 0: #check if the input is negative
            print("Please enter a non-negative number.")
            failed_entries += 1
            continue

        total_units = inventory + stock

        if total_units > 500: #check if the total units exceed 500
            print("Inventory limit cannot exceed 500 units. Please enter a smaller number.")
            failed_entries += 1
        else:
            inventory = total_units

    except ValueError:
        print("Please enter a valid number.")
        failed_entries += 1

    print("Current Inventory:", inventory)
    print("Failed Entries:", failed_entries)