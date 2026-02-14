from enum import Enum
from pydantic import BaseModel, Field, EmailStr
from uuid import UUID, uuid4
from typing import Optional

class DriverStatus(str, Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    SUSPENDED = "SUSPENDED"

class Driver(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str
    email: str = Field(..., pattern=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
    phone: str
    license: str
    status: DriverStatus = Field(default=DriverStatus.INACTIVE)
