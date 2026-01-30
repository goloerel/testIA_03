
import os
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database

# Use environment variable or default to local Docker instance
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DB_NAME = "fleet_management"

class DatabaseClient:
    client: MongoClient = None
    db: Database = None

    def connect(self):
        if not self.client:
            self.client = MongoClient(MONGODB_URL)
            self.db = self.client[DB_NAME]
            print(f"Connected to MongoDB at {MONGODB_URL}")

    def close(self):
        if self.client:
            self.client.close()
            self.client = None
            print("MongoDB connection closed")

    def get_collection(self, collection_name: str) -> Collection:
        if self.db is None:
            self.connect()
        return self.db[collection_name]

db_client = DatabaseClient()

def get_db_client():
    return db_client
