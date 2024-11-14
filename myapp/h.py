
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# MongoDB setup
uri = "mongodb+srv://vmodalla:1234@cluster0.znmzl.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri, server_api=ServerApi('1'))
database = client.get_database("users")
users_collection = database.get_collection("rankings")
user_collection1 = database.get_collection("users")

def update_all_user_ids(users_collection):
    """Update the '_id' field for all documents to be the username."""
    
    # Get all documents from the users_collection
    documents = users_collection.find()

    for doc in documents:
        # If the '_id' is an ObjectId, we don't need to change it
        
        user = list(doc.keys())[1]
         
            # Create a new document with the new '_id' and same content
        new_doc = doc.copy()
        new_doc['_id'] = user
            # Remove the old document
        users_collection.delete_one({'_id': doc['_id']})

            # Insert the new document with the updated '_id'
        users_collection.insert_one(new_doc)

         
            
    print("All documents have been updated.")
update_all_user_ids(users_collection)