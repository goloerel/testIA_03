from enum import Enum
from pydantic import BaseModel, Field, field_validator
from uuid import UUID, uuid4
from typing import Optional

class VehicleType(str, Enum):
    SEDAN = "SEDAN"
    TRUCK = "TRUCK"
    SUV = "SUV"
    VAN = "VAN"
    BUS = "BUS"

class Vehicle(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    make: str
    model: str
    year: int = Field(..., ge=1990, le=2026)
    vehicle_type: VehicleType
    fuel_type: str

    @field_validator("vehicle_type", mode="before")
    @classmethod
    def validate_enum_uppercase(cls, v: str) -> str:
        if isinstance(v, str):
            return v.upper()
        return v
