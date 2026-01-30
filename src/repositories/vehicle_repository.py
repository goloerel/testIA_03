from src.database import db_client
from typing import Dict, Optional
from bson import ObjectId

class VehicleRepository:
    def __init__(self):
        self.collection_name = "vehicles"

    def get_collection(self):
        return db_client.get_collection(self.collection_name)

    def create(self, vehicle_data: Dict) -> Dict:
        result = self.get_collection().insert_one(vehicle_data)
        vehicle_data["_id"] = str(result.inserted_id)
        return vehicle_data

    def get_by_id(self, vehicle_id: str) -> Optional[Dict]:
        return self.get_collection().find_one({"_id": ObjectId(vehicle_id)})

    def update(self, vehicle_id: str, vehicle_data: Dict) -> Optional[Dict]:
        return self.get_collection().find_one_and_update(
            {"_id": ObjectId(vehicle_id)},
            {"$set": vehicle_data},
            return_document=True
        )

    def delete(self, vehicle_id: str) -> bool:
        result = self.get_collection().delete_one({"_id": ObjectId(vehicle_id)})
        return result.deleted_count > 0

    def get_by_placa(self, placa: str) -> Optional[Dict]:
        return self.get_collection().find_one({"placa": placa})

    def get_by_numero_economico(self, numero_economico: str) -> Optional[Dict]:
        return self.get_collection().find_one({"numero_economico": numero_economico})

    def list_vehicles(self, limit: int, offset: int):
        return self.get_collection().find().skip(offset).limit(limit)

    def count_vehicles(self) -> int:
        return self.get_collection().count_documents({})

vehicle_repository = VehicleRepository()
