from flask import Flask, render_template
import json
import sqlite3
from ai import generate
import jsonify

# Database connection string (replace with your actual connection details)


# Define SQLAlchemy base class (optional, adjust based on your model)




# Create engine and session maker
def convert_item(item):
  return {
      "Name": item[0],
      "Quantity": 10,  # Replace with your default quantity if needed
      "ExpiryDate": item[2]
  }


# Initialize Flask app
app = Flask(__name__)

# Function to get data from database
def get_items():
  conn = sqlite3.connect("items.db")
  cursor = conn.cursor()
  item = cursor.execute("SELECT * FROM category;")
  all_entries = cursor.fetchall()
  cursor.close()
  conn.close()
# Print the retrieved entries (optional)
  json_data = json.dumps(all_entries)
  converted_data = [convert_item(item) for item in all_entries]
 #Convert the list to JSON string with desired formatting
  sample_json = json.dumps(converted_data, indent=4) 
  return sample_json

def create_db():
  conn = sqlite3.connect("items.db") 
   # Replace with your desired database file name

    # Create the 'category' table if it doesn't exist
  cursor = conn.cursor()
  cursor.execute('''CREATE TABLE IF NOT EXISTS category (
                        Name text PRIMARY KEY,
                        weight real,
                        expiration_date date
                        )''')
  conn.commit()  # Commit the table creation
  conn.close()

# Route to render the list page
@app.route('/')
def index():
  create_db()
  return render_template('home.html')


@app.route('/recipie')
async def recipie():
  x ="This the avaiable ingerients in my fridge "
  list = []
  sample_json = get_items()
  x = x + sample_json
  x = x + "\nWhat are the available dishes I can make. Provide available dishes as a json with dish name and ingredients required alsong with nutritional facts "
  
  result = await generate(x)
  if sample_json is None:
        # Handle the case where no ingredients are found (e.g., return error message)
        return jsonify({"error": "No ingredients found"})
  dishes = await generate(x)


  return render_template('recipies.html',dishes)
  





@app.route('/inv')
def inventory():
  
  # Sample JSON data (replace with your actual data fetching logic)
  sample_json = get_items()
  materials = json.loads(sample_json)  # Convert JSON string to a list of dictionaries

  return render_template('inventory.html', materials=materials)

if __name__ == '__main__':
  app.run(debug=True)
