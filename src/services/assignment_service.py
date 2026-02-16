from typing import List, Optional
from datetime import datetime
from src.repositories.assignment_repository import AssignmentRepository
from src.repositories.driver_repository import DriverRepository
from src.repositories.vehicle_repository import VehicleRepository
from src.schemas.assignment import AssignmentInput, Assignment, AssignmentStatus, AssignmentUpdate
from src.core.exceptions import (
    VehicleAlreadyAssignedError,
    DriverAlreadyAssignedError,
    AssignmentNotFoundError,
    DriverNotFoundError,
    VehicleNotFoundError
)

class AssignmentService:
    def __init__(
        self, 
        assignment_repository: AssignmentRepository,
        driver_repository: DriverRepository,
        vehicle_repository: VehicleRepository
    ):
        self.assignment_repository = assignment_repository
        self.driver_repository = driver_repository
        self.vehicle_repository = vehicle_repository

    def create_assignment(self, input_data: AssignmentInput) -> Assignment:
        # 1. Validate Existences
        if not self.driver_repository.get_by_id(input_data.driver_id):
            raise DriverNotFoundError(f"Driver {input_data.driver_id} not found.")
            
        if not self.vehicle_repository.get_by_id(input_data.vehicle_id):
            raise VehicleNotFoundError(f"Vehicle {input_data.vehicle_id} not found.")

        # 2. Validate Constraints (Active Assignments)
        if self.assignment_repository.find_active_by_driver(input_data.driver_id):
            raise DriverAlreadyAssignedError(f"Driver {input_data.driver_id} already has an active assignment.")

        if self.assignment_repository.find_active_by_vehicle(input_data.vehicle_id):
            raise VehicleAlreadyAssignedError(f"Vehicle {input_data.vehicle_id} already has an active assignment.")

        # 3. Create
        data = input_data.model_dump()
        data["estado"] = AssignmentStatus.ACTIVE
        data["fecha_creacion"] = datetime.now()
        
        created = self.assignment_repository.create(data)
        return Assignment(**created)

    def get_assignment(self, id: str) -> Assignment:
        doc = self.assignment_repository.get_by_id(id)
        if not doc:
            raise AssignmentNotFoundError(f"Assignment {id} not found.")
        return Assignment(**doc)

    def update_assignment(self, id: str, update_data: AssignmentUpdate) -> Assignment:
        # Check existence
        if not self.assignment_repository.get_by_id(id):
            raise AssignmentNotFoundError(f"Assignment {id} not found.")

        # Perform update
        # Note: If updating status to COMPLETED, we might want validation, 
        # but pure data update is allowed here as per schema.
        updated = self.assignment_repository.update(id, update_data.model_dump(exclude_unset=True))
        if not updated:
             raise AssignmentNotFoundError(f"Assignment {id} not found during update.")
             
        return Assignment(**updated)
    
    def list_assignments(self, limit: int, offset: int) -> List[Assignment]:
        docs = self.assignment_repository.list_assignments(limit, offset)
        return [Assignment(**d) for d in docs]
