from flask import Flask, render_template
import json
import random



# Database connection string (replace with your actual connection details)


# Define SQLAlchemy base class (optional, adjust based on your model)




# Create engine and session maker


# Initialize Flask app
app = Flask(__name__)

# Function to get data from database
def get_items():
  items = []
  for i in range (0,10):
    item = random.randint(1,10000)
    items.append(item)
  return items

# Route to render the list page
@app.route('/')
def index():
  items = get_items()  # Call the data fetching function
  return render_template('home.html', items=items)

@app.route('/inv')
def inventory():
  # Sample JSON data (replace with your actual data fetching logic)
  sample_json = '[{"Name": "Item 1", "Quantity": 10, "ExpiryDate": "2024-11-20"}, {"Name": "Item 2", "Quantity": 5}, {"Name": "Item 3", "Quantity": 2, "ExpiryDate": "2025-01-15"},{"Name": "Item 3", "Quantity": 2, "ExpiryDate": "2025-01-15"}]'
  materials = json.loads(sample_json)  # Convert JSON string to a list of dictionaries

  return render_template('inventory.html', materials=materials)

if __name__ == '__main__':
  app.run(debug=True)
