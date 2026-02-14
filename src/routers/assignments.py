from fastapi import APIRouter, status
from src.models.assignment import Assignment
from src.services.assignment_service import assignment_service

router = APIRouter(prefix="/assignments", tags=["Assignments"])

@router.post("/", response_model=Assignment, status_code=status.HTTP_201_CREATED)
def create_assignment(assignment: Assignment):
    return assignment_service.create_assignment(assignment)

@router.post("/{assignment_id}/complete")
def complete_assignment(assignment_id: str):
    return assignment_service.complete_assignment(assignment_id)
