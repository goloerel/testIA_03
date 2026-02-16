from fastapi import APIRouter, Depends
from src.schemas.stats import StatsResponse
from src.services.stats_service import StatsService
from src.repositories.vehicle_repository import VehicleRepository
from src.repositories.driver_repository import DriverRepository
from src.repositories.assignment_repository import AssignmentRepository

router = APIRouter(
    prefix="/api/v1/stats",
    tags=["stats"]
)

# Dependency Factory
def get_stats_service():
    return StatsService(
        vehicle_repository=VehicleRepository(),
        driver_repository=DriverRepository(),
        assignment_repository=AssignmentRepository()
    )

@router.get("/", response_model=StatsResponse)
def get_stats(service: StatsService = Depends(get_stats_service)):
    return service.get_stats()
