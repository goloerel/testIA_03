from fastapi import APIRouter, status, Depends, HTTPException
from typing import List

from src.schemas.assignment import Assignment, AssignmentInput, AssignmentUpdate
from src.services.assignment_service import AssignmentService
from src.repositories.assignment_repository import AssignmentRepository
from src.repositories.driver_repository import DriverRepository
from src.repositories.vehicle_repository import VehicleRepository
from src.core.exceptions import (
    VehicleAlreadyAssignedError,
    DriverAlreadyAssignedError,
    AssignmentNotFoundError,
    DriverNotFoundError,
    VehicleNotFoundError
)

router = APIRouter(
    prefix="/api/v1/assignments",
    tags=["assignments"]
)

# Dependency Factory
def get_assignment_service():
    return AssignmentService(
        assignment_repository=AssignmentRepository(),
        driver_repository=DriverRepository(),
        vehicle_repository=VehicleRepository()
    )

@router.post("/", response_model=Assignment, status_code=status.HTTP_201_CREATED)
def create_assignment(
    input_data: AssignmentInput, 
    service: AssignmentService = Depends(get_assignment_service)
):
    try:
        return service.create_assignment(input_data)
    except (DriverNotFoundError, VehicleNotFoundError) as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except (DriverAlreadyAssignedError, VehicleAlreadyAssignedError) as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))

@router.get("/", response_model=List[Assignment])
def list_assignments(
    limit: int = 10, 
    offset: int = 0,
    service: AssignmentService = Depends(get_assignment_service)
):
    return service.list_assignments(limit, offset)

@router.get("/{id}", response_model=Assignment)
def get_assignment(
    id: str,
    service: AssignmentService = Depends(get_assignment_service)
):
    try:
        return service.get_assignment(id)
    except AssignmentNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.put("/{id}", response_model=Assignment)
def update_assignment(
    id: str, 
    update_data: AssignmentUpdate,
    service: AssignmentService = Depends(get_assignment_service)
):
    try:
        return service.update_assignment(id, update_data)
    except AssignmentNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
