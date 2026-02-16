from src.database import db_client
from typing import Dict, Optional, List, Any
from bson import ObjectId

class VehicleRepository:
    def __init__(self):
        self.collection_name = "vehicles"

    def get_collection(self):
        return db_client.get_collection(self.collection_name)

    def _fix_id(self, doc: Dict) -> Dict:
        if doc and "_id" in doc:
            doc["_id"] = str(doc["_id"])
        return doc

    def create(self, vehicle_data: Dict) -> Dict:
        result = self.get_collection().insert_one(vehicle_data)
        vehicle_data["_id"] = str(result.inserted_id)
        return vehicle_data

    def get_by_id(self, vehicle_id: str) -> Optional[Dict]:
        if not ObjectId.is_valid(vehicle_id):
            return None
        doc = self.get_collection().find_one({"_id": ObjectId(vehicle_id)})
        return self._fix_id(doc) if doc else None

    def update(self, vehicle_id: str, vehicle_data: Dict) -> Optional[Dict]:
        if not ObjectId.is_valid(vehicle_id):
            return None
        doc = self.get_collection().find_one_and_update(
            {"_id": ObjectId(vehicle_id)},
            {"$set": vehicle_data},
            return_document=True
        )
        return self._fix_id(doc) if doc else None

    def delete(self, vehicle_id: str) -> bool:
        if not ObjectId.is_valid(vehicle_id):
            return False
        result = self.get_collection().delete_one({"_id": ObjectId(vehicle_id)})
        return result.deleted_count > 0

    def get_by_placa(self, placa: str) -> Optional[Dict]:
        doc = self.get_collection().find_one({"placa": placa})
        return self._fix_id(doc) if doc else None

    def get_by_numero_economico(self, numero_economico: str) -> Optional[Dict]:
        doc = self.get_collection().find_one({"numero_economico": numero_economico})
        return self._fix_id(doc) if doc else None

    def list_vehicles(self, limit: int, offset: int) -> List[Dict]:
        cursor = self.get_collection().find().skip(offset).limit(limit)
        return [self._fix_id(doc) for doc in cursor]

    def count_vehicles(self) -> int:
        return self.get_collection().count_documents({})

    def count_by_status(self, status: str) -> int:
        return self.get_collection().count_documents({"estado_vehiculo": status})

vehicle_repository = VehicleRepository()
