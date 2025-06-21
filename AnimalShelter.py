# AnimalShelter.py
from pymongo import MongoClient
from bson.objectid import ObjectId
from urllib.parse import quote_plus

class AnimalShelter:
    def __init__(self, user='aacuser', password='potato',
                host='nv-desktop-services.apporto.com', port=30702,
                db='AAC', col='animals'):
        try:
            user_encoded = quote_plus(user)
            password_encoded = quote_plus(password)
            uri = f"mongodb://{user_encoded}:{password_encoded}@{host}:{port}"
            self.client = MongoClient(uri)
            self.database = self.client[db]
            self.collection = self.database[col]
        except Exception as e:
            print(f"Error connecting to the MongoDB: {e}")
            raise

    def create(self, data):
        """Inserts a document into the collection"""
        if data:
            try:
                result = self.collection.insert_one(data)
                return result.acknowledged
            except Exception as e:
                print(f"Insert failed: {e}")
                return False
        else:
            raise Exception("Nothing to save because data parameter is empty")

    def read(self, query):
        """Reads documents from the collection matching the query"""
        try:
            results = self.collection.find(query)
            return list(results)
        except Exception as e:
            print(f"Read failed: {e}")
            return []

    def update(self, query, update_data, multiple=False):
        # Update documents based on the query
        try:
            if multiple:
                result = self.collection.update_many(query, update_data)
            else:
                result = self.collection.update_one(query, update_data)
            return result.modified_count
        except Exception as e:
            print("Update failed:", e)
            return 0
        
    def delete(self, query, multiple=False):
        # Delete documents based on the query
        try:
            if multiple:
                result = self.collection.delete_many(query)
            else:
                result = self.collection.delete_one(query)
            return result.deleted_count
        except Exception as e:
            print("Delete failed:", e)
            return 0
