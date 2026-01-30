from datetime import date, datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field, constr

class VehicleType(str, Enum):
    TRACTOR_TRUCK = "TRACTOR_TRUCK"
    RIGID_TRUCK = "RIGID_TRUCK"
    TRAILER = "TRAILER"
    DOLLY = "DOLLY"

class VehicleStatus(str, Enum):
    ACTIVE = "ACTIVE"
    IN_MAINTENANCE = "IN_MAINTENANCE"
    OUT_OF_SERVICE = "OUT_OF_SERVICE"

class FuelType(str, Enum):
    DIESEL = "DIESEL"
    NATURAL_GAS = "NATURAL_GAS"
    ELECTRIC = "ELECTRIC"

class VehicleInput(BaseModel):
    placa: str = Field(..., pattern=r'^[A-Z0-9]{2,3}-[A-Z0-9]{3,5}$', description="Mexican license plate format")
    numero_economico: str
    marca: str
    modelo: str
    anno: int = Field(..., ge=1990, le=2026)
    tipo_vehiculo: VehicleType
    capacidad_carga_kg: float = Field(..., gt=0)
    numero_serie: str = Field(..., min_length=17, max_length=17)
    estado_vehiculo: VehicleStatus
    poliza_seguro: str
    vigencia_seguro: date
    kilometraje_actual: int = Field(..., ge=0)
    tipo_combustible: FuelType

    model_config = ConfigDict(
        populate_by_name=True,
        json_schema_extra={
            "example": {
                "placa": "ABC-1234",
                "numero_economico": "MTY-105",
                "marca": "Kenworth",
                "modelo": "T680",
                "anno": 2024,
                "tipo_vehiculo": "TRACTOR_TRUCK",
                "capacidad_carga_kg": 35000.0,
                "numero_serie": "1NKDL4XDXMP123456",
                "estado_vehiculo": "ACTIVE",
                "poliza_seguro": "QUALITAS-998877",
                "vigencia_seguro": "2027-01-29",
                "kilometraje_actual": 15000,
                "tipo_combustible": "DIESEL"
            }
        }
    )

class Vehicle(VehicleInput):
    id: str = Field(..., alias="_id")
    fecha_alta: datetime
    ultima_verificacion: Optional[datetime] = None

    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True
    )
