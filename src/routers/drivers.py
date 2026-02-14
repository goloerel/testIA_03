from fastapi import APIRouter, status
from src.models.driver import Driver
from src.services.driver_service import driver_service

router = APIRouter(prefix="/drivers", tags=["Drivers"])

@router.post("/", response_model=Driver, status_code=status.HTTP_201_CREATED)
def create_driver(driver: Driver):
    return driver_service.create_driver(driver)

@router.post("/{driver_id}/suspend")
def suspend_driver(driver_id: str):
    return driver_service.suspend_driver(driver_id)
