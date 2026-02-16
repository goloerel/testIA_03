from src.database import db_client
from typing import Dict, Optional, List
from bson import ObjectId

class DriverRepository:
    def __init__(self):
        self.collection_name = "drivers"

    def get_collection(self):
        return db_client.get_collection(self.collection_name)

    def _fix_id(self, doc: Dict) -> Dict:
        if doc and "_id" in doc:
            doc["_id"] = str(doc["_id"])
        return doc

    def create(self, driver_data: Dict) -> Dict:
        result = self.get_collection().insert_one(driver_data)
        driver_data["_id"] = str(result.inserted_id)
        return driver_data

    def get_by_id(self, driver_id: str) -> Optional[Dict]:
        if not ObjectId.is_valid(driver_id):
            return None
        doc = self.get_collection().find_one({"_id": ObjectId(driver_id)})
        return self._fix_id(doc) if doc else None

    def get_by_license(self, licencia: str) -> Optional[Dict]:
        doc = self.get_collection().find_one({"licencia": licencia})
        return self._fix_id(doc) if doc else None

    def update(self, driver_id: str, driver_data: Dict) -> Optional[Dict]:
        if not ObjectId.is_valid(driver_id):
            return None
        doc = self.get_collection().find_one_and_update(
            {"_id": ObjectId(driver_id)},
            {"$set": driver_data},
            return_document=True
        )
        return self._fix_id(doc) if doc else None

    def delete(self, driver_id: str) -> bool:
        if not ObjectId.is_valid(driver_id):
            return False
        result = self.get_collection().delete_one({"_id": ObjectId(driver_id)})
        return result.deleted_count > 0

    def list_drivers(self, limit: int, offset: int) -> List[Dict]:
        cursor = self.get_collection().find().skip(offset).limit(limit)
        return [self._fix_id(doc) for doc in cursor]

    def count_drivers(self) -> int:
        return self.get_collection().count_documents({})

    def count_by_status(self, status: str) -> int:
        return self.get_collection().count_documents({"estado": status})

driver_repository = DriverRepository()
