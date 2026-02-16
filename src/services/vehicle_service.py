from typing import List, Optional
from src.repositories.vehicle_repository import VehicleRepository
from src.schemas.vehicle import VehicleInput, Vehicle
from src.core.exceptions import VehicleAlreadyExistsError, VehicleNotFoundError

from datetime import datetime

class VehicleService:
    def __init__(self, repository: VehicleRepository):
        self.repository = repository

    def create_vehicle(self, vehicle_input: VehicleInput) -> Vehicle:
        # Check for duplicates by Composite Keys (as per requirements/logic)
        # 1. Check Placa
        if self.repository.get_by_placa(vehicle_input.placa):
             raise VehicleAlreadyExistsError(f"Vehicle with license plate {vehicle_input.placa} already exists.")
        
        # 2. Check Economic Number
        if self.repository.get_by_numero_economico(vehicle_input.numero_economico):
            raise VehicleAlreadyExistsError(f"Vehicle with economic number {vehicle_input.numero_economico} already exists.")

        # Prepare data
        vehicle_dict = vehicle_input.model_dump()
        vehicle_dict["fecha_alta"] = datetime.now()
        
        # Add metadata (simulating what was in the original schema default factories if needed)
        # For now, just passing the dict to repo. Repo handles ID generation.
        
        created_data = self.repository.create(vehicle_dict)
        return Vehicle(**created_data)

    def list_vehicles(self, limit: int, offset: int) -> List[Vehicle]:
        vehicles_data = self.repository.list_vehicles(limit, offset)
        return [Vehicle(**v) for v in vehicles_data]

    def get_vehicle(self, vehicle_id: str) -> Vehicle:
        vehicle_data = self.repository.get_by_id(vehicle_id)
        if not vehicle_data:
            raise VehicleNotFoundError(f"Vehicle with ID {vehicle_id} not found.")
        return Vehicle(**vehicle_data)

    def update_vehicle(self, vehicle_id: str, vehicle_input: VehicleInput) -> Vehicle:
        # Check if exists first
        if not self.repository.get_by_id(vehicle_id):
            raise VehicleNotFoundError(f"Vehicle with ID {vehicle_id} not found.")

        # Update
        updated_data = self.repository.update(vehicle_id, vehicle_input.model_dump())
        # If concurrency concern, updated_data could still be None if deleted in between
        if not updated_data:
             raise VehicleNotFoundError(f"Vehicle with ID {vehicle_id} not found during update.")
             
        return Vehicle(**updated_data)

    def delete_vehicle(self, vehicle_id: str) -> None:
        if not self.repository.get_by_id(vehicle_id):
            raise VehicleNotFoundError(f"Vehicle with ID {vehicle_id} not found.")
            
        success = self.repository.delete(vehicle_id)
        if not success:
            # Should have been caught by get_by_id unless race condition
             raise VehicleNotFoundError(f"Delete failed for ID {vehicle_id}.")
