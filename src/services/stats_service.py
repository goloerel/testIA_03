from src.repositories.vehicle_repository import VehicleRepository
from src.repositories.driver_repository import DriverRepository
from src.repositories.assignment_repository import AssignmentRepository
from src.schemas.stats import StatsResponse
from src.schemas.vehicle import VehicleStatus
from src.schemas.driver import DriverStatus
from src.schemas.assignment import AssignmentStatus

class StatsService:
    def __init__(
        self,
        vehicle_repository: VehicleRepository,
        driver_repository: DriverRepository,
        assignment_repository: AssignmentRepository
    ):
        self.vehicle_repository = vehicle_repository
        self.driver_repository = driver_repository
        self.assignment_repository = assignment_repository

    def get_stats(self) -> StatsResponse:
        return StatsResponse(
            vehicles_total=self.vehicle_repository.count_vehicles(),
            vehicles_active=self.vehicle_repository.count_by_status(VehicleStatus.ACTIVE.value),
            vehicles_maintenance=self.vehicle_repository.count_by_status(VehicleStatus.IN_MAINTENANCE.value),
            drivers_total=self.driver_repository.count_drivers(),
            drivers_active=self.driver_repository.count_by_status(DriverStatus.ACTIVE.value),
            assignments_active=self.assignment_repository.count_by_status(AssignmentStatus.ACTIVE.value)
        )
