from typing import List, Optional
from datetime import datetime
from src.repositories.driver_repository import DriverRepository
from src.schemas.driver import DriverInput, Driver
from src.core.exceptions import DriverAlreadyExistsError, DriverNotFoundError

class DriverService:
    def __init__(self, repository: DriverRepository):
        self.repository = repository

    def create_driver(self, driver_input: DriverInput) -> Driver:
        # Check for duplicates by License
        if self.repository.get_by_license(driver_input.licencia):
            raise DriverAlreadyExistsError(f"Driver with license {driver_input.licencia} already exists.")

        # Prepare data
        driver_dict = driver_input.model_dump()
        driver_dict["fecha_creacion"] = datetime.now()
        
        created_data = self.repository.create(driver_dict)
        return Driver(**created_data)

    def list_drivers(self, limit: int, offset: int) -> List[Driver]:
        drivers_data = self.repository.list_drivers(limit, offset)
        return [Driver(**d) for d in drivers_data]

    def get_driver(self, driver_id: str) -> Driver:
        driver_data = self.repository.get_by_id(driver_id)
        if not driver_data:
            raise DriverNotFoundError(f"Driver with ID {driver_id} not found.")
        return Driver(**driver_data)

    def update_driver(self, driver_id: str, driver_input: DriverInput) -> Driver:
        # Check if exists first
        if not self.repository.get_by_id(driver_id):
            raise DriverNotFoundError(f"Driver with ID {driver_id} not found.")

        # Check license uniqueness if changing license
        existing_license = self.repository.get_by_license(driver_input.licencia)
        if existing_license and str(existing_license["_id"]) != driver_id:
             raise DriverAlreadyExistsError(f"Driver with license {driver_input.licencia} already exists.")

        # Update
        updated_data = self.repository.update(driver_id, driver_input.model_dump())
        if not updated_data:
             raise DriverNotFoundError(f"Driver with ID {driver_id} not found during update.")
             
        return Driver(**updated_data)

    def delete_driver(self, driver_id: str) -> None:
        if not self.repository.get_by_id(driver_id):
            raise DriverNotFoundError(f"Driver with ID {driver_id} not found.")
            
        success = self.repository.delete(driver_id)
        if not success:
             raise DriverNotFoundError(f"Delete failed for ID {driver_id}.")
