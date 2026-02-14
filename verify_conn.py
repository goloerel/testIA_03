import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")

def test_connection():
    try:
        client = MongoClient(MONGODB_URL, serverSelectionTimeoutMS=2000)
        client.admin.command('ping')
        print("Successfully connected to MongoDB container!")
    except ConnectionFailure:
        print("Failed to connect to MongoDB container. Is it running?")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    test_connection()
