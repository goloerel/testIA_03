from fastapi import HTTPException
from src.database import db_client
from src.models.vehicle import Vehicle

class VehicleService:
    def __init__(self):
        self.collection = db_client.get_collection("vehicles")

    def create_vehicle(self, vehicle: Vehicle):
        # Brief: Validate duplicates (409 Conflict if already exists)
        # We'll check by make, model, year as a composite key for "exists"
        existing = self.collection.find_one({
            "make": vehicle.make,
            "model": vehicle.model,
            "year": vehicle.year
        })
        if existing:
            raise HTTPException(status_code=409, detail="Vehicle already exists")
        
        vehicle_dict = vehicle.model_dump()
        vehicle_dict["id"] = str(vehicle_dict["id"])
        
        self.collection.insert_one(vehicle_dict)
        return vehicle

vehicle_service = VehicleService()
