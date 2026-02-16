from datetime import date, datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

class DriverStatus(str, Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"

class DriverInput(BaseModel):
    nombre: str = Field(..., min_length=1, description="Full name of the driver")
    licencia: str = Field(..., min_length=1, description="Driver's license number (Unique)")
    estado: DriverStatus = DriverStatus.ACTIVE
    fecha_contratacion: date

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
        json_schema_extra={
            "example": {
                "nombre": "Juan Perez",
                "licencia": "MX-DL-12345",
                "estado": "ACTIVE",
                "fecha_contratacion": "2024-01-15"
            }
        }
    )

class Driver(DriverInput):
    id: str = Field(..., alias="_id")
    fecha_creacion: datetime

    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True
    )
