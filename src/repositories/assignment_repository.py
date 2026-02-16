from src.database import db_client
from typing import Dict, Optional, List
from bson import ObjectId
from src.schemas.assignment import AssignmentStatus

class AssignmentRepository:
    def __init__(self):
        self.collection_name = "assignments"

    def get_collection(self):
        return db_client.get_collection(self.collection_name)

    def _fix_id(self, doc: Dict) -> Dict:
        if doc and "_id" in doc:
            doc["_id"] = str(doc["_id"])
        return doc

    def create(self, data: Dict) -> Dict:
        result = self.get_collection().insert_one(data)
        data["_id"] = str(result.inserted_id)
        return data

    def get_by_id(self, id: str) -> Optional[Dict]:
        if not ObjectId.is_valid(id):
            return None
        doc = self.get_collection().find_one({"_id": ObjectId(id)})
        return self._fix_id(doc) if doc else None

    def find_active_by_vehicle(self, vehicle_id: str) -> Optional[Dict]:
        doc = self.get_collection().find_one({
            "vehicle_id": vehicle_id,
            "estado": AssignmentStatus.ACTIVE.value
        })
        return self._fix_id(doc) if doc else None

    def find_active_by_driver(self, driver_id: str) -> Optional[Dict]:
        doc = self.get_collection().find_one({
            "driver_id": driver_id,
            "estado": AssignmentStatus.ACTIVE.value
        })
        return self._fix_id(doc) if doc else None

    def update(self, id: str, data: Dict) -> Optional[Dict]:
        if not ObjectId.is_valid(id):
            return None
        doc = self.get_collection().find_one_and_update(
            {"_id": ObjectId(id)},
            {"$set": data},
            return_document=True
        )
        return self._fix_id(doc) if doc else None

    def list_assignments(self, limit: int, offset: int) -> List[Dict]:
        cursor = self.get_collection().find().skip(offset).limit(limit)
        return [self._fix_id(doc) for doc in cursor]


    def count_assignments(self) -> int:
        return self.get_collection().count_documents({})

    def count_by_status(self, status: str) -> int:
        return self.get_collection().count_documents({"estado": status})

assignment_repository = AssignmentRepository()
