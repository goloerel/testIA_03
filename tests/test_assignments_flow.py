from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from src.main import app
from src.api.assignments import get_assignment_service
from src.services.assignment_service import AssignmentService

client = TestClient(app)

mock_assignment_data = {
    "_id": "507f1f77bcf86cd799439099",
    "driver_id": "507f1f77bcf86cd799439011",
    "vehicle_id": "507f1f77bcf86cd799439012",
    "fecha_inicio": "2024-02-01",
    "observaciones": "Initial assignment",
    "estado": "ACTIVE",
    "fecha_creacion": "2024-02-01T10:00:00"
}

def get_mock_service(mock_repo, mock_d, mock_v):
    return AssignmentService(
        assignment_repository=mock_repo,
        driver_repository=mock_d,
        vehicle_repository=mock_v
    )

def test_get_assignment():
    mock_repo = MagicMock()
    mock_repo.get_by_id.return_value = mock_assignment_data
    
    app.dependency_overrides[get_assignment_service] = lambda: get_mock_service(mock_repo, MagicMock(), MagicMock())
    
    try:
        response = client.get("/api/v1/assignments/507f1f77bcf86cd799439099")
        assert response.status_code == 200
        assert response.json()["_id"] == "507f1f77bcf86cd799439099"
    finally:
        app.dependency_overrides = {}

def test_end_assignment():
    mock_repo = MagicMock()
    # Exists
    mock_repo.get_by_id.return_value = mock_assignment_data
    # Update return
    updated_data = {**mock_assignment_data, "estado": "COMPLETED", "fecha_fin": "2024-02-15"}
    mock_repo.update.return_value = updated_data
    
    app.dependency_overrides[get_assignment_service] = lambda: get_mock_service(mock_repo, MagicMock(), MagicMock())
    
    try:
        payload = {"estado": "COMPLETED", "fecha_fin": "2024-02-15"}
        response = client.put("/api/v1/assignments/507f1f77bcf86cd799439099", json=payload)
        
        assert response.status_code == 200
        assert response.json()["estado"] == "COMPLETED"
    finally:
        app.dependency_overrides = {}
