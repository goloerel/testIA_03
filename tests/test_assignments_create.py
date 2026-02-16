from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from src.main import app
from src.api.assignments import get_assignment_service
from src.services.assignment_service import AssignmentService

client = TestClient(app)

valid_assignment_payload = {
    "driver_id": "507f1f77bcf86cd799439011",
    "vehicle_id": "507f1f77bcf86cd799439012",
    "fecha_inicio": "2024-02-01",
    "observaciones": "Initial assignment"
}

def get_mock_service(mock_repo, mock_driver_repo, mock_vehicle_repo):
    return AssignmentService(
        assignment_repository=mock_repo,
        driver_repository=mock_driver_repo,
        vehicle_repository=mock_vehicle_repo
    )

def test_create_assignment_success():
    mock_repo = MagicMock()
    mock_driver_repo = MagicMock()
    mock_vehicle_repo = MagicMock()
    
    # 1. Existence checks
    mock_driver_repo.get_by_id.return_value = {"_id": "507f1f77bcf86cd799439011"}
    mock_vehicle_repo.get_by_id.return_value = {"_id": "507f1f77bcf86cd799439012"}
    
    # 2. Active assignment checks (None = no active assignment)
    mock_repo.find_active_by_driver.return_value = None
    mock_repo.find_active_by_vehicle.return_value = None
    
    # 3. Create
    mock_repo.create.side_effect = lambda x: {**x, "_id": "507f1f77bcf86cd799439099"}
    
    app.dependency_overrides[get_assignment_service] = lambda: get_mock_service(mock_repo, mock_driver_repo, mock_vehicle_repo)

    try:
        response = client.post("/api/v1/assignments/", json=valid_assignment_payload)
        
        assert response.status_code == 201
        data = response.json()
        assert data["estado"] == "ACTIVE"
    finally:
        app.dependency_overrides = {}

def test_create_assignment_driver_conflict():
    mock_repo = MagicMock()
    mock_driver_repo = MagicMock()
    mock_vehicle_repo = MagicMock()
    
    # Existence
    mock_driver_repo.get_by_id.return_value = {"_id": "507f1f77bcf86cd799439011"}
    mock_vehicle_repo.get_by_id.return_value = {"_id": "507f1f77bcf86cd799439012"}
    
    # Driver already assigned
    mock_repo.find_active_by_driver.return_value = {"_id": "active_assignment_id"}
    
    app.dependency_overrides[get_assignment_service] = lambda: get_mock_service(mock_repo, mock_driver_repo, mock_vehicle_repo)

    try:
        response = client.post("/api/v1/assignments/", json=valid_assignment_payload)
        
        assert response.status_code == 409
        assert "Driver" in response.json()["detail"]
    finally:
        app.dependency_overrides = {}
