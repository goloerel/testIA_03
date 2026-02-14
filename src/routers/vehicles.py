from fastapi import APIRouter, status
from src.models.vehicle import Vehicle
from src.services.vehicle_service import vehicle_service

router = APIRouter(prefix="/vehicles", tags=["Vehicles"])

@router.post("/", response_model=Vehicle, status_code=status.HTTP_201_CREATED)
def create_vehicle(vehicle: Vehicle):
    return vehicle_service.create_vehicle(vehicle)
