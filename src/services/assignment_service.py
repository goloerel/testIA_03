from datetime import datetime
from fastapi import HTTPException
from src.database import db_client
from src.models.assignment import Assignment, AssignmentStatus
from src.models.driver import DriverStatus
from typing import List

class AssignmentService:
    def __init__(self):
        self.assignment_collection = db_client.get_collection("assignments")
        self.driver_collection = db_client.get_collection("drivers")
        self.vehicle_collection = db_client.get_collection("vehicles")

    def create_assignment(self, assignment: Assignment):
        driver_id_str = str(assignment.driver_id)
        vehicle_id_str = str(assignment.vehicle_id)

        # 1. Validation: The Driver must exist and be INACTIVE.
        driver = self.driver_collection.find_one({"id": driver_id_str})
        if not driver:
            raise HTTPException(status_code=400, detail="Driver does not exist")
        if driver["status"] != DriverStatus.INACTIVE:
            raise HTTPException(status_code=400, detail="Driver is not INACTIVE")

        # 2. Multiplicity: A vehicle accepts up to 2 drivers.
        # Check active assignments for this vehicle during this time range?
        # The brief says "A vehicle accepts up to 2 drivers". 
        # Usually this means at any given time.
        overlapping_vehicle = self.assignment_collection.count_documents({
            "vehicle_id": vehicle_id_str,
            "status": {"$in": [AssignmentStatus.ACTIVE, AssignmentStatus.INACTIVE]},
            "$or": [
                {"start_date": {"$lt": assignment.end_date}, "end_date": {"$gt": assignment.start_date}}
            ]
        })
        if overlapping_vehicle >= 2:
            raise HTTPException(status_code=400, detail="Vehicle already has 2 drivers assigned for this period")

        # 3. Multiplicity: A driver has 0 time overlaps.
        overlapping_driver = self.assignment_collection.find_one({
            "driver_id": driver_id_str,
            "status": {"$in": [AssignmentStatus.ACTIVE, AssignmentStatus.INACTIVE]},
            "$or": [
                {"start_date": {"$lt": assignment.end_date}, "end_date": {"$gt": assignment.start_date}}
            ]
        })
        if overlapping_driver:
            raise HTTPException(status_code=400, detail="Driver has overlapping assignments")

        # 4. Time Trigger: If start_date == now, Driver and Assignment become ACTIVE.
        now = datetime.now()
        # Using a small threshold (e.g. 1 minute) or just checking if start_date <= now
        if assignment.start_date <= now:
            assignment.status = AssignmentStatus.ACTIVE
            # Update driver status
            self.driver_collection.update_one(
                {"id": driver_id_str},
                {"$set": {"status": DriverStatus.ACTIVE}}
            )

        assignment_dict = assignment.model_dump()
        assignment_dict["id"] = str(assignment_dict["id"])
        assignment_dict["driver_id"] = str(assignment_dict["driver_id"])
        assignment_dict["vehicle_id"] = str(assignment_dict["vehicle_id"])

        self.assignment_collection.insert_one(assignment_dict)
        return assignment

    def complete_assignment(self, assignment_id: str):
        # 5. Completion: Upon completion, Driver returns to INACTIVE and Assignment to COMPLETED.
        assignment = self.assignment_collection.find_one({"id": assignment_id})
        if not assignment:
            raise HTTPException(status_code=404, detail="Assignment not found")
        
        self.assignment_collection.update_one(
            {"id": assignment_id},
            {"$set": {"status": AssignmentStatus.COMPLETED, "end_date": datetime.now()}}
        )
        self.driver_collection.update_one(
            {"id": assignment["driver_id"]},
            {"$set": {"status": DriverStatus.INACTIVE}}
        )
        return {"message": "Assignment completed"}

assignment_service = AssignmentService()
