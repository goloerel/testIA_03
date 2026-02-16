from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from src.main import app
from src.api.vehicles import get_vehicle_service
from src.services.vehicle_service import VehicleService

client = TestClient(app)

def get_mock_service(mock_repo):
    return VehicleService(repository=mock_repo)

def test_delete_vehicle_success():
    mock_repo = MagicMock()
    # Mock existence check for delete
    mock_repo.get_by_id.return_value = {"_id": "507f1f77bcf86cd799439011"}
    # Mock effective delete
    mock_repo.delete.return_value = True
    
    app.dependency_overrides[get_vehicle_service] = lambda: get_mock_service(mock_repo)

    try:
        response = client.delete("/api/v1/vehicles/507f1f77bcf86cd799439011")
        assert response.status_code == 204
    finally:
        app.dependency_overrides = {}

def test_delete_vehicle_not_found():
    mock_repo = MagicMock()
    # Mock not found
    mock_repo.get_by_id.return_value = None
    
    app.dependency_overrides[get_vehicle_service] = lambda: get_mock_service(mock_repo)

    try:
        response = client.delete("/api/v1/vehicles/507f1f77bcf86cd799439011")
        assert response.status_code == 404
        assert "not found" in response.json()["detail"]
    finally:
        app.dependency_overrides = {}
