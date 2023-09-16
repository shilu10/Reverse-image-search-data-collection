
from pymongo.mongo_client import MongoClient

uri = "mongodb+srv://shilu:shilu@cluster0.uwihc6i.mongodb.net/?retryWrites=true&w=majority"

# Create a new client and connect to the server
client = MongoClient(uri)

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)


db = client['labels'] 

collection = db['labels_collection']

data = {
	'class_name': "tiger",
	"class_id": 1 
}

collection.insert_one(data)


docs = [doc for doc in collection.find()]

print(docs)