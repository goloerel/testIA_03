from fastapi import APIRouter, status
from src.schemas.vehicle import Vehicle, VehicleInput
from src.services.vehicle_service import vehicle_service

router = APIRouter(
    prefix="/api/v1/vehicles",
    tags=["vehicles"]
)

@router.post("/", response_model=Vehicle, status_code=status.HTTP_201_CREATED)
def create_vehicle(vehicle: VehicleInput):
    return vehicle_service.create_vehicle(vehicle)

@router.get("/")
def list_vehicles(limit: int = 10, offset: int = 0):
    return vehicle_service.list_vehicles(limit, offset)

@router.get("/{id}", response_model=Vehicle)
def get_vehicle(id: str):
    return vehicle_service.get_vehicle(id)

@router.put("/{id}", response_model=Vehicle)
def update_vehicle(id: str, vehicle: VehicleInput):
    return vehicle_service.update_vehicle(id, vehicle)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_vehicle(id: str):
    vehicle_service.delete_vehicle(id)
