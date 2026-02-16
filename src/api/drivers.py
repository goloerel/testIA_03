from fastapi import APIRouter, status, Depends, HTTPException
from typing import List

from src.schemas.driver import Driver, DriverInput
from src.services.driver_service import DriverService
from src.repositories.driver_repository import DriverRepository
from src.core.exceptions import DriverAlreadyExistsError, DriverNotFoundError

router = APIRouter(
    prefix="/api/v1/drivers",
    tags=["drivers"]
)

# Dependency Factory
def get_driver_service():
    repository = DriverRepository()
    return DriverService(repository)

@router.post("/", response_model=Driver, status_code=status.HTTP_201_CREATED)
def create_driver(
    driver: DriverInput, 
    service: DriverService = Depends(get_driver_service)
):
    try:
        return service.create_driver(driver)
    except DriverAlreadyExistsError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))

@router.get("/", response_model=List[Driver])
def list_drivers(
    limit: int = 10, 
    offset: int = 0,
    service: DriverService = Depends(get_driver_service)
):
    return service.list_drivers(limit, offset)

@router.get("/{id}", response_model=Driver)
def get_driver(
    id: str,
    service: DriverService = Depends(get_driver_service)
):
    try:
        return service.get_driver(id)
    except DriverNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.put("/{id}", response_model=Driver)
def update_driver(
    id: str, 
    driver: DriverInput,
    service: DriverService = Depends(get_driver_service)
):
    try:
        return service.update_driver(id, driver)
    except DriverNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except DriverAlreadyExistsError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_driver(
    id: str,
    service: DriverService = Depends(get_driver_service)
):
    try:
        service.delete_driver(id)
    except DriverNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
