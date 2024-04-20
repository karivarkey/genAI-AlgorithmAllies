#import cv2  # Optional, for future barcode scanning implementation (if needed)
import numpy as np
import sqlite3  # For database interaction
from datetime import date, timedelta  # For expiry date handling


def process_item(item, conn):
    """
    Processes an item based on its category and writes details to the database.

    Args:
        item (str): The name of the item (can be empty).
        conn (sqlite3.Connection): A connection object to the database.
    """

    cursor = conn.cursor()

    if item.lower().startswith("veg_"):
        # Extract vegetable name from the format
        vegetable_name = item[4:]

        # Simulate weight sensor reading (replace with actual sensor code)
        weight = round(np.random.uniform(0.1, 1.5), 2)  # Random weight between 0.1 and 1.5 kg

        # Add 5 days to current date for expiry
        today = date.today()
        expiry_date = (today + timedelta(days=5)).strftime("%Y-%m-%d")

        # Write data to database
        cursor.execute("INSERT INTO category (Name, weight, expiration_date) VALUES (?, ?, ?)",
                       (vegetable_name, weight, expiry_date))
        conn.commit()

        print(f"Detected vegetable: {vegetable_name}. Weight: {weight} kg. Expiry: {expiry_date} (written to database)")

    elif item.lower().startswith("pac_"):
        # Extract packaged food name prefix from the format
        food_prefix = item[:4]

        # Dummy barcode scan (replace with actual implementation)
        barcode_data = scan_barcode(dummy=True)
        # Example dummy barcode data format: "name,weight,expiry"
        if barcode_data:
            name, weight, expiry_date = barcode_data.split(",")

            # Write data to database
            cursor.execute("INSERT INTO category (Name, weight, expiration_date) VALUES (?, ?, ?)",
                           (name, float(weight), expiry_date))
            conn.commit()

            print(f"Scanned barcode for {food_prefix} food: Name: {name}, Weight: {weight}, Expiry: {expiry_date} (written to database)")
        else:
            print(f"Failed to scan barcode for {food_prefix} food.")

    else:
        # Handle undetected items
        print("Undetected item. Please enter details:")

        while True:
            try:
                name = input("Enter item name: ")
                weight = float(input("Enter weight (kg): "))
                # Validate expiry date format (YYYY-MM-DD)
                expiry_date = input("Enter expiry date (YYYY-MM-DD): ")
                date.fromisoformat(expiry_date)  # Raise ValueError for invalid format
                break
            except ValueError:
                print("Invalid expiry date format. Please enter YYYY-MM-DD.")

        # Write data to database
        cursor.execute("INSERT INTO category (Name, weight, expiration_date) VALUES (?, ?, ?)",
                       (name, weight, expiry_date))
        conn.commit()

        print(f"Added item: {name}, Weight: {weight} kg, Expiry: {expiry_date} (written to database)")


def scan_barcode(dummy=True):
    """
    Dummy barcode scanning function (replace with actual implementation).

    Args:
        dummy (bool, optional): Flag to indicate dummy behavior (default: True).

    Returns:
        str: A dummy barcode string in the format "name,weight,expiry" (for demonstration).
    """

    if dummy:
        return "Product 1.25,2024-06-20"  # Dummy barcode data with name, weight, expiry
    else:
        # Replace with your code to capture frames from a camera and use a barcode library
        # like pyzbar to decode the barcode. You'll need to extract relevant information
        # (name, weight, expiry) from the decoded data.
        pass


# Main function for user interaction
def main():
    # Connect to the database
    conn = sqlite3.connect("items.db")  # Replace with your desired database file name

    # Create the 'category' table if it doesn't exist
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS category (
                        Name text PRIMARY KEY,
                        weight real,
                        expiration_date date
                        )''')
    conn.commit()  # Commit the table creation

    # Now you can proceed with using the database in the loop
    while True:
        item = input("Enter item (veg_<name>, pac_<name>, or name for other items): ")

        # Function call to process the item
        process_item(item, conn)  # Here's the call to process_item

        # Ask user if they want to add another item
        choice = input("Add another item? (y/n): ")
        if choice.lower() != "y":
            break

    # Remember to close the connection after the loop
    conn.close()


if __name__ == "__main__":
    main()
