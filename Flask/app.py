from flask import Flask, render_template
import json
import sqlite3
from ai import generate
import yaml

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
  x = x + """\nWhat are the available dishes I can make. Provide available dishes along with nutritional values in a proper json format Keep the json simple and minimal with 0 comments. Act like an API returning the JSON. DO NOT ADD COMMENTS AND ALL VALUE MUST BE STRINGS. 22g of a nutrient must be shows as '22g'. The details must be , name , ingrideint , nutrition. the nutrition will have 4 sub values of calories , prootiens , carbohydfrates and fats DO NOT USE OTHER NAMES FOR JSON VALUES, Strictly follow this example
{
  "availableDishes": [
    {
      "name": "Tomato Salad",
      "ingredients": "tomato",
      "nutrition": {
        "calories": "18kcal",
        "proteins": "0.9g",
        "carbohydrates": "3.9g",
        "fats": "0.2g"
      }
    },
    {
      "name": "Tomato and Lays Snack Mix",
      "ingredients": "tomato, Lays",
      "nutrition": {
        "calories": "Varies based on Lays flavor",
        "proteins": "Varies based on Lays flavor",
        "carbohydrates": "Varies based on Lays flavor",
        "fats": "Varies based on Lays flavor" 
      }
    } 
  ]
}
 """
  is_loading = True
  print("Showing loader...")
  data_to_display  = await generate(x)
  print("Hiding loader...")
  is_loading = False
  with open('test.json','r') as f:
    list = json.load(f)
  print(list)
# Print the description with line breaks
  #return render_template('recipies.html',dishes=list['availableDishes'])
  return render_template('loading.html', content=f"<h1>'hello'</h1>")

  
  





@app.route('/inv')
def inventory():
  
  # Sample JSON data (replace with your actual data fetching logic)
  sample_json = get_items()
  materials = json.loads(sample_json)  # Convert JSON string to a list of dictionaries

  return render_template('inventory.html', materials=materials)

if __name__ == '__main__':
  app.run(debug=True)
