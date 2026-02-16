from pydantic import BaseModel, ConfigDict, Field

class StatsResponse(BaseModel):
    vehicles_total: int = Field(..., description="Total number of vehicles")
    vehicles_active: int = Field(..., description="Number of active vehicles")
    vehicles_maintenance: int = Field(..., description="Number of vehicles in maintenance")
    drivers_total: int = Field(..., description="Total number of drivers")
    drivers_active: int = Field(..., description="Number of active drivers")
    assignments_active: int = Field(..., description="Number of active assignments")

    model_config = ConfigDict(
        populate_by_name=True,
        json_schema_extra={
            "example": {
                "vehicles_total": 50,
                "vehicles_active": 45,
                "vehicles_maintenance": 5,
                "drivers_total": 60,
                "drivers_active": 55,
                "assignments_active": 40
            }
        }
    )
