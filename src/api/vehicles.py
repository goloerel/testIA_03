from fastapi import APIRouter, status, Depends, HTTPException
from typing import List

from src.schemas.vehicle import Vehicle, VehicleInput
from src.services.vehicle_service import VehicleService
from src.repositories.vehicle_repository import VehicleRepository
from src.core.exceptions import VehicleAlreadyExistsError, VehicleNotFoundError

router = APIRouter(
    prefix="/api/v1/vehicles",
    tags=["vehicles"]
)

# Dependency Factory
def get_vehicle_service():
    repository = VehicleRepository()
    return VehicleService(repository)

@router.post("/", response_model=Vehicle, status_code=status.HTTP_201_CREATED)
def create_vehicle(
    vehicle: VehicleInput, 
    service: VehicleService = Depends(get_vehicle_service)
):
    try:
        return service.create_vehicle(vehicle)
    except VehicleAlreadyExistsError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))

@router.get("/", response_model=List[Vehicle])
def list_vehicles(
    limit: int = 10, 
    offset: int = 0,
    service: VehicleService = Depends(get_vehicle_service)
):
    return service.list_vehicles(limit, offset)

@router.get("/{id}", response_model=Vehicle)
def get_vehicle(
    id: str,
    service: VehicleService = Depends(get_vehicle_service)
):
    try:
        return service.get_vehicle(id)
    except VehicleNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.put("/{id}", response_model=Vehicle)
def update_vehicle(
    id: str, 
    vehicle: VehicleInput,
    service: VehicleService = Depends(get_vehicle_service)
):
    try:
        return service.update_vehicle(id, vehicle)
    except VehicleNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_vehicle(
    id: str,
    service: VehicleService = Depends(get_vehicle_service)
):
    try:
        service.delete_vehicle(id)
    except VehicleNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
