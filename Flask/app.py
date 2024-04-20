from flask import Flask, render_template
import json
import sqlite3
from Flask.recipes_ai import generate
from Flask.vision_ai import classify_object
import jsonify
import base64
from flask import request
import asyncio


# Create engine and session maker
def convert_item(item):
  return {
      "Name": item[0],
      "Quantity": 10,  # Replace with your default quantity if needed
      "ExpiryDate": item[2]
  }

#item added:
item = 'empty'

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


@app.route('/add_items')
def add():
    return render_template('add_items/object_detection.html')

"""
@app.route('/scan')
def scan():
    return render_template('scan.html')

@app.route('/entry')
def entry():
    return render_template('entry.html')
"""
import asyncio

@app.route('/capture-image', methods=['POST'])
def capture_image():
  try:
    data =  request.get_json()
    image_data = data['imageData']
    
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(classify_object(image_data))
    print("this is the item: ", item)

    # Decode image data and save the image
    #image_bytes = base64.b64decode(image_data.split(',')[1])
    #with open('captured_image.jpg', 'wb') as f:
    #  f.write(image_bytes)

    return "Image captured successfully!", 200

  except Exception as e:
    print(f"Error capturing image: {e}")
    return "Error capturing image", 500
    
"""
@app.route('/submit-item', methods=['POST'])
def submit_item():
    try:
        data = request.get_json()
        name = data['name']
        expiry_date = data['expiryDate']
        weight = data['weight']

        # Save item details to your database or perform other backend actions
        # ... (store name, expiry_date, and weight in your database)

        return "Item details submitted successfully!", 200

    except Exception as e:
        print(f"Error submitting item: {e}")
        return "Error submitting item", 500

if __name__ == '__main__':
  app.run(debug=True)

  """