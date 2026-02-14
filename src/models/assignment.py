from enum import Enum
from pydantic import BaseModel, Field
from uuid import UUID, uuid4
from datetime import datetime
from typing import Optional

class AssignmentStatus(str, Enum):
    INACTIVE = "INACTIVE"
    ACTIVE = "ACTIVE"
    COMPLETED = "COMPLETED"
    DELAYED = "DELAYED"

class Assignment(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    driver_id: UUID
    vehicle_id: UUID
    start_date: datetime
    end_date: datetime
    origin: str
    destination: str
    status: AssignmentStatus = Field(default=AssignmentStatus.INACTIVE)
