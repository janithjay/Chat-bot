from pymongo import MongoClient

# Replace the following with your MongoDB connection string
connection_string = "mongodb+srv://janithjayashan018:janithjayashan018@cluster0.pvp1j.mongodb.net/"

# Create a MongoClient
client = MongoClient(connection_string)

# Access the database
db = client['pizza-bot']

# Access the collection
collection = db['contact_details']

# Fetch data
data = collection.find()

# Print fetched data
for document in data:
    print(document)