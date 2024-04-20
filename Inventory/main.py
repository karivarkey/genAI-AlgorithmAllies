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
        # Check for existing vegetable
        cursor.execute("SELECT weight FROM category WHERE Name = ?", (vegetable_name,))
        existing_weight = cursor.fetchone()

        if existing_weight:
          # Update weight for existing vegetable
          new_weight = weight + existing_weight[0]
          cursor.execute("UPDATE category SET weight = ? WHERE Name = ?", (new_weight, vegetable_name))
          conn.commit()
          print(f"Vegetable: {vegetable_name}. New weight: {new_weight} kg (existing weight + {weight} kg).")
        else:
          # Write new vegetable data to database
          cursor.execute("INSERT INTO category (Name, weight, expiration_date) VALUES (?, ?, ?)",
                          (vegetable_name, weight, expiry_date))
          print(f"Detected vegetable: {vegetable_name}. Weight: {weight} kg. Expiry: {expiry_date} (written to database)")
          conn.commit()

        

    elif item.lower().startswith("pac_"):
  
        name = input("Enter item name:")  # Can be used if needed

  # Dummy barcode scan (replace with actual implementation)
        barcode_data = scan_barcode(dummy=True)

  # Check if barcode data is valid (not None)
        if barcode_data:
            weight, expiry_date = barcode_data.split(",")
            weight = float(weight)

            # Check for existing packaged food with the same name
            cursor.execute("SELECT weight FROM category WHERE Name = ?", (name,))
            existing_weight = cursor.fetchone()

            if existing_weight:
                # Check if existing_weight[0] is a number (float) before adding
                if isinstance(existing_weight[0], float):
                    new_weight = weight + existing_weight[0]
                    cursor.execute("UPDATE category SET weight = ? WHERE Name = ?", (new_weight, name))
                    conn.commit()
                    print(f"Updated weight for {name}: Name: {name}, Weight: {new_weight} kg, Expiry: {expiry_date} (written to database)")
                else:
                    print(f"Error: Unexpected data type for existing weight of {name}.")
            else:
                # Write data to database for new packaged food
                cursor.execute("INSERT INTO category (Name, weight, expiration_date) VALUES (?, ?, ?)",
                                (name, float(weight), expiry_date))
                conn.commit()
                print(f"Added packaged food: {name}. Weight: {weight} kg, Expiry: {expiry_date} (written to database)")
        else:
            # Handle case where barcode scan fails (or no barcode for pac_ items)
            print(f"No barcode data available for {name}. Enter weight:")
            weight = float(input())  # Prompt user for weight

            # Write data to database with weight from user input
            cursor.execute("INSERT INTO category (Name, weight, expiration_date) VALUES (?, ?, ?)",
                            (name, weight, expiry_date))  # Assuming expiry_date is obtained elsewhere
            conn.commit()
            print(f"Added packaged food: {name}. Weight: {weight} kg, Expiry: {expiry_date} (written to database)")


    else:  # Handle undetected items
        print("Undetected item. Please enter details:")

        while True:
            try:
                name = input("Enter item name: ")
                weight = float(input("Enter weight (kg): "))

                # Check for existing item in database
                cursor.execute("SELECT weight FROM category WHERE Name = ?", (name,))
                existing_weight = cursor.fetchone()

                if existing_weight:
                    # Update weight for existing item
                    new_weight = weight + existing_weight[0]
                    cursor.execute("UPDATE category SET weight = ? WHERE Name = ?", (new_weight, name))
                    conn.commit()
                    print(f"Updated weight for {name}: Name: {name}, Weight: {new_weight} kg (written to database)")
                    break
                else:
                    # Validate expiry date format (YYYY-MM-DD)
                    expiry_date = input("Enter expiry date (YYYY-MM-DD): ")
                    date.fromisoformat(expiry_date)  # Raise ValueError for invalid format

                    # Add new item to database
                    cursor.execute("INSERT INTO category (Name, weight, expiration_date) VALUES (?, ?, ?)",
                                    (name, weight, expiry_date))
                    conn.commit()
                    print(f"Added new item: {name}. Weight: {weight} kg, Expiry: {expiry_date} (written to database)")
                    break

            except ValueError:
                print("Invalid expiry date format. Please enter YYYY-MM-DD.")


                


def scan_barcode(dummy=True):
    """
    Dummy barcode scanning function (replace with actual implementation).

    Args:
        dummy (bool, optional): Flag to indicate dummy behavior (default: True).

    Returns:
        str: A dummy barcode string in the format "name,weight,expiry" (for demonstration).
    """

    if dummy:
        return "1.25,2024-06-20"  # Dummy barcode data with weight, expiry
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
