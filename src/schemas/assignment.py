from datetime import date, datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

class AssignmentStatus(str, Enum):
    ACTIVE = "ACTIVE"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"

class AssignmentInput(BaseModel):
    driver_id: str = Field(..., description="ID of the driver")
    vehicle_id: str = Field(..., description="ID of the vehicle")
    fecha_inicio: date = Field(default_factory=date.today)
    observaciones: Optional[str] = None

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
        json_schema_extra={
            "example": {
                "driver_id": "507f1f77bcf86cd799439011",
                "vehicle_id": "507f1f77bcf86cd799439012",
                "fecha_inicio": "2024-02-01",
                "observaciones": "Initial assignment"
            }
        }
    )

class AssignmentUpdate(BaseModel):
    fecha_fin: Optional[date] = None
    estado: Optional[AssignmentStatus] = None
    nota_cierre: Optional[str] = None

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True
    )

class Assignment(AssignmentInput):
    id: str = Field(..., alias="_id")
    estado: AssignmentStatus = AssignmentStatus.ACTIVE
    fecha_fin: Optional[date] = None
    nota_cierre: Optional[str] = None
    fecha_creacion: datetime

    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True
    )
