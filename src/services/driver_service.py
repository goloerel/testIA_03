from fastapi import HTTPException
from src.database import db_client
from src.models.driver import Driver, DriverStatus

class DriverService:
    def __init__(self):
        self.collection = db_client.get_collection("drivers")

    def create_driver(self, driver: Driver):
        # Brief: Validate license uniqueness (409 Conflict)
        existing = self.collection.find_one({"license": driver.license})
        if existing:
            raise HTTPException(status_code=409, detail="Driver license already exists")
        
        driver_dict = driver.model_dump()
        driver_dict["id"] = str(driver_dict["id"])
        
        self.collection.insert_one(driver_dict)
        return driver

    def suspend_driver(self, driver_id: str):
        # Brief: Do not delete, use SUSPENDED.
        result = self.collection.update_one(
            {"id": driver_id},
            {"$set": {"status": DriverStatus.SUSPENDED}}
        )
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Driver not found")
        return {"message": "Driver suspended"}

    def get_driver_by_id(self, driver_id: str):
        driver = self.collection.find_one({"id": driver_id})
        if not driver:
            raise HTTPException(status_code=404, detail="Driver not found")
        return driver

driver_service = DriverService()
